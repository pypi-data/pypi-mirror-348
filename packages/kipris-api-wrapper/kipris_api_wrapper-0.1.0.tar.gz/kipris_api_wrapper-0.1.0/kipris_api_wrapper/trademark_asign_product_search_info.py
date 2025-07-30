# 생성 2025/05/08 22:24 AI개발자
# 수정 2025/04/29 12:59 코드에이전트 (리팩토링된 내부 함수 테스트하도록 수정 및 ImportError 수정)
# 수정 2025/04/29 13:18 아키텍트 (대체 XML 구조 파싱 오류 및 simm 누락 처리 수정)

"""
KIPRIS 상품명 키워드 검색 API (trademarkAsignProductSearchInfo) 처리 로직 (내부용)
"""

import logging
import httpx # http_client 타입 힌트용
from typing import Optional, List, Dict, Any
from lxml import etree
from pydantic import ValidationError

# 내부 모듈 임포트
from .core import _request_helpers # 코어 헬퍼 임포트
from .models import ProductCodeSearchResponse, ProductCodeInfo
from .exceptions import (
    KiprisApiClientError,
    KiprisApiError,
    KiprisApiParsingError,
    MissingAPIKeyError,
    KiprisTooManyResultsError,
    KiprisApiKeyError
)
from . import utils
from . import config

logger = logging.getLogger(__name__)

async def _search_internal(
    http_client: httpx.AsyncClient,
    api_key: str,
    endpoint: str,
    product_keyword: str,
    rows: int = 100,
    page_no: int = 1,
) -> ProductCodeSearchResponse:
    """
    (내부 함수) KIPRIS 상품명 키워드 검색 API (trademarkAsignProductSearchInfo)를 호출하고 결과를 파싱합니다.
    KiprisClient에 의해 호출됩니다.

    Args:
        http_client: 사용할 httpx.AsyncClient 인스턴스.
        api_key: 사용할 KIPRIS API 키.
        endpoint: 호출할 API 엔드포인트.
        product_keyword: 검색할 상품/서비스 명칭 키워드.
        rows: 페이지당 결과 수.
        page_no: 페이지 번호.

    Returns:
        ProductCodeSearchResponse: 검색 결과 (파싱된 모델).

    Raises:
        KiprisApiClientError: API 호출 실패 또는 파라미터 처리 중 예상치 못한 오류 발생 시.
        KiprisApiError: KIPRIS API 자체 오류 시 ('04' 제외).
        KiprisApiKeyError: KIPRIS API 키 오류('04') 발생 시 (_request_helpers에서 발생).
        KiprisApiParsingError: 응답 파싱 실패 시.
        KiprisTooManyResultsError: 결과 건수가 임계값을 초과할 경우.
        ValueError: 파라미터 값이 잘못된 경우.
    """
    # 파라미터 검증
    if not product_keyword or not product_keyword.strip():
        raise ValueError("상품 키워드(product_keyword)는 필수 파라미터입니다.")
    if not isinstance(rows, int) or rows <= 0:
        raise ValueError(f"rows 파라미터는 양의 정수여야 합니다: {rows}")
    if not isinstance(page_no, int) or page_no <= 0:
        raise ValueError(f"page_no 파라미터는 양의 정수여야 합니다: {page_no}")

    # API 파라미터 준비 (API 키 제외)
    params = {
        "searchWord": product_keyword,
        "docsCount": rows,
        "docsStart": page_no, # KIPRIS API는 pageNo 대신 docsStart 사용
    }

    # 파라미터 인코딩 (utils 사용)
    encoded_params = utils.encode_special_chars_in_params(params)

    try:
        # --- _request_helpers.make_api_request 호출 ---
        response: httpx.Response = await _request_helpers.make_api_request(
            http_client=http_client,
            endpoint=endpoint,
            params=encoded_params,
            api_key=api_key
        )
        # ---------------------------------------------

        # --- XML 파싱 및 모델 변환 로직 ---
        try:
            if not response.content:
                 logger.info(f"Empty response body for {endpoint}, returning empty result.")
                 return ProductCodeSearchResponse(total_count=0, results=[])

            root = etree.fromstring(response.content)
            # 헤더는 _request_helpers에서 검증됨
            body = root.find(".//body")
            if body is None:
                 logger.warning(f"Missing body element in KIPRIS response for {endpoint}, returning empty result.")
                 return ProductCodeSearchResponse(total_count=0, results=[])

            # API 스펙에 따라 다양한 응답 구조 처리
            items_element = body.find("items")
            # items 태그 없이 body 바로 아래에 여러 개의 trademarkAsignProductSearchInfo 태그가 올 수 있음
            trademark_info_elements = body.findall("trademarkAsignProductSearchInfo")

            if items_element is None and not trademark_info_elements:
                logger.warning(f"Neither 'items' nor 'trademarkAsignProductSearchInfo' element found in response for {endpoint}, returning empty result.")
                return ProductCodeSearchResponse(total_count=0, results=[])

            # count 요소를 통한 전체 결과 수 파악
            count_element = root.find(".//count")
            total_search_count_elem = None
            if items_element is not None:
                total_search_count_elem = items_element.find("totalSearchCount")

            total_count = -1 # 기본값
            if count_element is not None or total_search_count_elem is not None:
                total_count_str = None
                if total_search_count_elem is not None:
                    total_count_str = total_search_count_elem.text
                elif count_element is not None:
                    total_count_str = count_element.findtext("totalCount")

                try:
                    total_count = int(total_count_str.strip()) if total_count_str and total_count_str.strip() else 0
                except (ValueError, TypeError) as e:
                    raise KiprisApiParsingError(f"Invalid totalCount value: '{total_count_str}' for {endpoint}") from e
            else:
                 logger.warning(f"Missing count element in response for {endpoint}. Total count unknown.")


            logger.info(f"Parsed total product info count for {endpoint}: {total_count}")

            # --- 결과 건수 임계값 초과 확인 ---
            if total_count >= 0 and total_count >= config.KIPRIS_RESULT_COUNT_THRESHOLD:
                error_msg = f"KIPRIS returned excessively many results ({total_count} >= {config.KIPRIS_RESULT_COUNT_THRESHOLD}) for {endpoint}. This likely indicates an issue with the request parameters or an API bug."
                logger.error(error_msg, extra={"request_params": params}) # 인코딩 전 파라미터 로깅
                raise KiprisTooManyResultsError(
                    total_count=total_count,
                    threshold=config.KIPRIS_RESULT_COUNT_THRESHOLD,
                    request_params=params
                )
            # ---------------------------------

            parsed_results: List[ProductCodeInfo] = []

            # items 아래의 trademarkAsignProductSearchInfo 처리
            if items_element is not None:
                item_elements = items_element.findall("trademarkAsignProductSearchInfo")
                logger.debug(f"Found {len(item_elements)} trademarkAsignProductSearchInfo elements under 'items' tag in XML for {endpoint}.")
                for item_element in item_elements:
                    _parse_product_item_internal(item_element, parsed_results) # 내부 헬퍼 호출

            # body 바로 아래의 trademarkAsignProductSearchInfo 처리 (대체 구조)
            elif trademark_info_elements:
                logger.debug(f"Found {len(trademark_info_elements)} trademarkAsignProductSearchInfo elements directly under 'body' tag in XML for {endpoint}.")
                for item_element in trademark_info_elements: # findall 결과를 순회
                    _parse_product_item_internal(item_element, parsed_results)

            logger.info(f"Successfully parsed {len(parsed_results)} product items for {endpoint}.")
            return ProductCodeSearchResponse(total_count=total_count, results=parsed_results)

        except etree.XMLSyntaxError as e:
            error_content = response.text[:500]
            msg = f"KIPRIS API 응답 본문 XML 파싱 실패: {endpoint}"
            logger.error(f"{msg} - Response: {error_content}", exc_info=True)
            raise KiprisApiParsingError(msg) from e
        except KiprisTooManyResultsError:
            raise
        except Exception as e:
            logger.critical(f"Unexpected error during XML parsing/processing for {endpoint}: {e}", exc_info=True)
            raise KiprisApiParsingError(f"Unexpected parsing/processing error for {endpoint}: {e}") from e

    except (KiprisApiClientError, KiprisApiError, KiprisApiKeyError, KiprisApiParsingError, KiprisTooManyResultsError) as e:
        raise
    except ValueError as e: # 파라미터 값 검증 오류
        logger.error(f"Invalid parameter value provided for {endpoint}: {e}", exc_info=True)
        raise # ValueError는 그대로 전달
    except Exception as e: # 이 함수 내의 다른 예상치 못한 오류 (예: 파라미터 준비 단계)
        logger.critical(f"Unexpected error in _search_internal for {endpoint}: {e}", exc_info=True)
        raise KiprisApiClientError(f"Unexpected error processing parameters for {endpoint}: {e}") from e


def _parse_product_item_internal(item_element: etree._Element, results: List[ProductCodeInfo]):
    """
    (내부 헬퍼) trademarkAsignProductSearchInfo XML 요소를 파싱하여 ProductCodeInfo 모델로 변환하고 results 리스트에 추가합니다.
    파싱 또는 유효성 검사 실패 시 로깅하고 건너<0xEB><0x9A><0x8D>니다.
    """
    try:
        raw_item_data = {child.tag: child.text.strip() for child in item_element if child.text is not None}

        # 필수 필드 확인 (API 응답에 따라 조정 필요)
        required_fields = ['name', 'classsification'] # 'name' (상품명), 'classsification' (분류코드) - 'n' -> 'name' 수정
        if not all(field in raw_item_data for field in required_fields):
            logger.warning(f"Skipping product item due to missing required fields ({required_fields}). Raw data: {raw_item_data}")
            return

        # 데이터 매핑 및 변환
        similarity_codes_str = raw_item_data.get('simm', '') # simm 태그가 없거나 비어있으면 빈 문자열
        similarity_codes = [code.strip() for code in similarity_codes_str.split(',') if code.strip()] if similarity_codes_str else [] # 빈 리스트 처리

        mapped_data = {
            "product_name": raw_item_data.get('name'), # 'n' -> 'name' 수정
            "classification_code": raw_item_data.get('classsification'),
            "similarity_codes": similarity_codes, # 변환된 리스트 사용
            "product_name_en": raw_item_data.get('engName'),
            "product_description": raw_item_data.get('productsDesc'),
            "version": raw_item_data.get('version'),
            "product_number": raw_item_data.get('productsNum'),
            "is_main": raw_item_data.get('main') == 'true' if raw_item_data.get('main') else None,
        }
        # None 값 필터링
        filtered_mapped_data = {k: v for k, v in mapped_data.items() if v is not None}

        # Pydantic 모델 유효성 검사 및 생성
        product_info = ProductCodeInfo.model_validate(filtered_mapped_data)
        results.append(product_info)

    except ValidationError as e:
        logger.warning(f"Product item validation failed, skipping item: {e}. Raw data: {raw_item_data}", exc_info=True)
    except Exception as e: # pragma: no cover
        logger.error(f"Unexpected error parsing product item, skipping item: {e}. Raw data: {raw_item_data}", exc_info=True)