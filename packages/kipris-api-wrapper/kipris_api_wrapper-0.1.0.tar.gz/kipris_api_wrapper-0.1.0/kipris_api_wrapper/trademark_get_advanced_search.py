# 생성 2025/04/28 11:56 아키텍트
# 수정 2025/04/29 12:54 코드에이전트 (Phase 2 리팩토링: 내부 함수 구조 변경)
# 수정 2025/04/29 13:09 아키텍트 (파라미터 준비 로직 예외 처리 수정)
# 수정 2025/04/29 20:31 아키텍트 (번호 검색 파라미터 추가 및 필수 조건 검증)

"""
KIPRIS 상표 상세 검색 API (getAdvancedSearch) 처리 로직 (내부용)
"""

import logging
import httpx # http_client 타입 힌트용
from typing import Optional, List, Dict, Any
from lxml import etree
from pydantic import ValidationError

# 내부 모듈 임포트
from .core import _request_helpers # 코어 헬퍼 임포트
from .models import TrademarkSearchResponse, TrademarkItem
# KiprisApiKeyError는 client에서 처리하므로 여기서 직접 임포트할 필요 없음
from .exceptions import KiprisApiClientError, KiprisApiError, KiprisApiParsingError, MissingAPIKeyError, KiprisTooManyResultsError, KiprisApiKeyError # KiprisApiKeyError 추가 (make_api_request에서 발생 가능)
from . import utils
from . import config

logger = logging.getLogger(__name__)

# 함수 이름을 내부용으로 변경 (_search_internal)
# KiprisClient에서 필요한 http_client, api_key, endpoint를 인자로 받음
async def _search_internal(
    http_client: httpx.AsyncClient,
    api_key: str,
    endpoint: str,
    trademark_name: Optional[str] = None,
    classification_codes: Optional[List[str]] = None,
    similarity_codes: Optional[List[str]] = None,
    vienna_codes: Optional[List[str]] = None,
    applicant_name: Optional[str] = None,
    application_number: Optional[str] = None, # 출원번호 파라미터 추가
    registration_number: Optional[str] = None, # 등록번호 파라미터 추가
    rows: int = 100,
    page_no: int = 1,
) -> TrademarkSearchResponse:
    """
    (내부 함수) KIPRIS 상표 상세 검색 API (getAdvancedSearch)를 호출하고 결과를 파싱합니다.
    KiprisClient에 의해 호출됩니다.

    Args:
        http_client: 사용할 httpx.AsyncClient 인스턴스.
        api_key: 사용할 KIPRIS API 키.
        endpoint: 호출할 API 엔드포인트.
        trademark_name: 상표 명칭.
        classification_codes: NICE 분류 코드 리스트.
        similarity_codes: 유사군 코드 리스트.
        vienna_codes: 비엔나 코드 리스트.
        applicant_name: 출원인 명칭.
        application_number: 출원번호 (하이픈 포함 가능).
        registration_number: 등록번호 (하이픈 포함 가능).
        rows: 페이지당 결과 수.
        page_no: 페이지 번호.

    Returns:
        TrademarkSearchResponse: 검색 결과 (파싱된 모델).

    Raises:
        KiprisApiClientError: API 호출 실패 또는 파라미터 처리 중 예상치 못한 오류 발생 시.
        KiprisApiError: KIPRIS API 자체 오류 시 ('04' 제외).
        KiprisApiKeyError: KIPRIS API 키 오류('04') 발생 시 (_request_helpers에서 발생).
        KiprisApiParsingError: 응답 파싱 실패 시.
        KiprisTooManyResultsError: 결과 건수가 임계값을 초과할 경우.
        ValueError: 파라미터 값이 잘못된 경우 (필수 검색 조건 누락 포함).
    """
    # --- 필수 검색 조건 검증 ---
    if not any([trademark_name, classification_codes, similarity_codes, vienna_codes, applicant_name, application_number, registration_number]):
        raise ValueError("하나 이상의 검색 조건(상표명, 분류코드, 출원번호 등)을 입력해야 합니다.")

    # --- 파라미터 타입/값 검증 ---
    # 이 검증은 함수 초기에 수행하여 잘못된 호출을 빠르게 차단
    if not isinstance(rows, int) or rows <= 0:
        raise ValueError(f"rows 파라미터는 양의 정수여야 합니다: {rows}")
    if not isinstance(page_no, int) or page_no <= 0:
        raise ValueError(f"page_no 파라미터는 양의 정수여야 합니다: {page_no}")
    # -------------------------

    try:
        # --- 파라미터 준비 로직을 try 블록 안으로 이동 ---
        params: Dict[str, Any] = {
            "numOfRows": rows,
            "pageNo": page_no,
            # 필수 Boolean 파라미터
            "application": "true", "registration": "true", "refused": "true",
            "expiration": "true", "withdrawal": "true", "publication": "true",
            "cancel": "true", "abandonment": "true", "trademark": "true",
            "serviceMark": "true", "trademarkServiceMark": "true", "businessEmblem": "true",
            "collectiveMark": "true", "geoOrgMark": "true", "certMark": "true",
            "geoCertMark": "true", "character": "true", "figure": "true",
            "compositionCharacter": "true", "figureComposition": "true", "sound": "true",
            "fragrance": "true", "color": "true", "dimension": "true",
            "colorMixed": "true", "hologram": "true", "motion": "true",
            "visual": "true", "invisible": "true",
        }
        # 선택적 파라미터 추가
        if trademark_name:
            params["trademarkName"] = trademark_name
        if classification_codes:
            params["classification"] = "|".join(classification_codes)
        if similarity_codes:
            params["similarityCode"] = "|".join(similarity_codes)
        if vienna_codes:
            params["viennaCode"] = "|".join(vienna_codes)
        if applicant_name:
            params["applicantName"] = applicant_name
        # 번호 파라미터 추가 (하이픈 제거)
        if application_number:
            # 출원번호는 'application' 타입으로 API 파라미터 준비
            cleaned_app_num = utils.prepare_api_number_param(application_number, 'application')
            if cleaned_app_num:
                params["applicationNumber"] = cleaned_app_num
        if registration_number:
            # 등록번호는 'registration' 타입으로 API 파라미터 준비
            cleaned_reg_num = utils.prepare_api_number_param(registration_number, 'registration')
            if cleaned_reg_num:
                params["registerNumber"] = cleaned_reg_num

        # 파라미터 인코딩 (utils 사용)
        encoded_params = utils.encode_special_chars_in_params(params)
        # -------------------------------------------------

        # --- _request_helpers.make_api_request 호출 ---
        # API 키와 http_client를 전달
        response: httpx.Response = await _request_helpers.make_api_request(
            http_client=http_client,
            endpoint=endpoint,
            params=encoded_params, # 인코딩된 파라미터 전달
            api_key=api_key
        )
        # ---------------------------------------------

        # --- XML 파싱 및 모델 변환 로직 ---
        try:
            # 응답 본문 파싱
            if not response.content:
                 logger.info(f"Empty response body for {endpoint}, returning empty result.")
                 return TrademarkSearchResponse(total_count=0, items=[])

            root = etree.fromstring(response.content)
            # 헤더는 _request_helpers에서 이미 검증했으므로 여기서는 body만 확인
            body = root.find(".//body")
            if body is None:
                 logger.warning(f"Missing body element in KIPRIS response for {endpoint}, returning empty result.")
                 return TrademarkSearchResponse(total_count=0, items=[])

            items_element = body.find("items")
            count_element = root.find(".//count") # count는 body 바깥에 있을 수 있음

            if count_element is None:
                 raise KiprisApiParsingError(f"Missing count element in KIPRIS response for {endpoint}")
            total_count_str = count_element.findtext("totalCount")

            try:
                total_count = int(total_count_str.strip()) if total_count_str and total_count_str.strip() else 0
            except (ValueError, TypeError) as e:
                raise KiprisApiParsingError(f"Invalid totalCount value: '{total_count_str}' for {endpoint}") from e

            logger.info(f"Parsed total result count for {endpoint}: {total_count}")

            # --- 결과 건수 임계값 초과 확인 ---
            if total_count >= config.KIPRIS_RESULT_COUNT_THRESHOLD:
                error_msg = f"KIPRIS returned excessively many results ({total_count} >= {config.KIPRIS_RESULT_COUNT_THRESHOLD}) for {endpoint}. This likely indicates an issue with the request parameters or an API bug."
                logger.error(error_msg, extra={"request_params": params}) # 인코딩 전 파라미터 로깅
                raise KiprisTooManyResultsError(
                    total_count=total_count,
                    threshold=config.KIPRIS_RESULT_COUNT_THRESHOLD,
                    request_params=params # 인코딩 전 파라미터 전달
                )
            # ---------------------------------

            parsed_items: List[TrademarkItem] = []
            if items_element is not None:
                item_elements = items_element.findall("item")
                logger.debug(f"Found {len(item_elements)} item elements in XML for {endpoint}.")
                for item_element in item_elements:
                    raw_item_data = {child.tag: child.text.strip() for child in item_element if child.text is not None and child.text.strip()}
                    try:
                        # 기존 파싱 로직 유지
                        mapped_data = {
                            "index_no": raw_item_data.get("indexNo"),
                            "application_number": raw_item_data.get("applicationNumber"),
                            "application_date": raw_item_data.get("applicationDate"),
                            "publication_number": raw_item_data.get("publicationNumber"),
                            "publication_date": raw_item_data.get("publicationDate"),
                            "registration_number": raw_item_data.get("registrationNumber"),
                            "registration_date": raw_item_data.get("registrationDate"),
                            "applicant_name": raw_item_data.get("applicantName"),
                            "agent_name": raw_item_data.get("agentName"),
                            "vienna_code": raw_item_data.get("viennaCode"),
                            "trademark_name": raw_item_data.get("title"),
                            "image_url": raw_item_data.get("bigDrawing"),
                            "classification_code": raw_item_data.get("classificationCode"),
                            "application_status": raw_item_data.get("applicationStatus"),
                            "registration_privilege_name": raw_item_data.get("regPrivilegeName"),
                        }
                        filtered_mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
                        parsed_items.append(TrademarkItem.model_validate(filtered_mapped_data))
                    except ValidationError as e:
                        logger.warning(f"Trademark item validation failed for {endpoint}, skipping item: {e}. Raw data: {raw_item_data}", exc_info=True)
                    except Exception as e: # pragma: no cover
                         logger.error(f"Unexpected error parsing trademark item for {endpoint}, skipping item: {e}. Raw data: {raw_item_data}", exc_info=True)

            logger.info(f"Successfully parsed {len(parsed_items)} trademark items for {endpoint}.")
            return TrademarkSearchResponse(total_count=total_count, items=parsed_items)

        except etree.XMLSyntaxError as e:
            error_content = response.text[:500]
            msg = f"KIPRIS API 응답 본문 XML 파싱 실패: {endpoint}"
            logger.error(f"{msg} - Response: {error_content}", exc_info=True)
            raise KiprisApiParsingError(msg) from e
        except KiprisTooManyResultsError: # 임계값 초과 오류는 그대로 전달
            raise
        except Exception as e: # 파싱 중 예상치 못한 오류
            logger.critical(f"Unexpected error during XML parsing/processing for {endpoint}: {e}", exc_info=True)
            raise KiprisApiParsingError(f"Unexpected parsing/processing error for {endpoint}: {e}") from e

    # _request_helpers.make_api_request에서 발생한 예외들은 그대로 전달됨
    # (KiprisApiClientError, KiprisApiError, KiprisApiKeyError, KiprisApiParsingError)
    # KiprisTooManyResultsError는 위에서 처리됨
    except (KiprisApiClientError, KiprisApiError, KiprisApiKeyError, KiprisApiParsingError) as e:
        # 여기서 별도 로깅 없이 그대로 raise 하여 KiprisClient에서 처리하도록 함
        raise
    except ValueError as e: # 파라미터 값 검증 오류 (필수 조건 누락 포함)
        logger.error(f"Invalid parameter value provided for {endpoint}: {e}", exc_info=True)
        raise # ValueError는 그대로 전달
    except Exception as e: # 이 함수 내의 다른 예상치 못한 오류 (예: 파라미터 준비 단계)
        logger.critical(f"Unexpected error in _search_internal for {endpoint}: {e}", exc_info=True)
        # 일반 오류는 KiprisApiClientError로 변환하여 전달 (메시지 수정)
        raise KiprisApiClientError(f"Unexpected error processing parameters for {endpoint}: {e}") from e