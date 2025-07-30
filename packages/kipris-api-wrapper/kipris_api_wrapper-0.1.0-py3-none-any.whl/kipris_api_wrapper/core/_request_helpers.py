# 생성 2025/05/24 00:58 AI개발자
# 수정 2025/04/29 12:36 코드에이전트 (역할 명확화 및 API 키 오류 처리 수정)

"""
kipris_api_wrapper.core._request_helpers

KIPRIS API 요청 실행 및 기본 응답/오류 처리를 위한 헬퍼 함수 제공.
"""

import logging
from typing import Dict, Any
import httpx
from lxml import etree # 헤더 파싱을 위해 유지

# 내부 모듈 임포트 - 경로 주의
from ..exceptions import KiprisApiClientError, KiprisApiError, KiprisApiParsingError, KiprisApiKeyError # KiprisApiKeyError 추가
from .. import config # 타임아웃 설정 등을 위해 유지

logger = logging.getLogger(__name__)

# get_client 함수는 KiprisClient 내부에서 http_client를 관리하므로 제거됨

async def make_api_request(
    http_client: httpx.AsyncClient, # httpx 클라이언트 직접 받음
    endpoint: str,
    params: Dict[str, Any],
    api_key: str, # API 키 직접 받음
    method: str = "GET"
) -> httpx.Response: # 반환 타입을 httpx.Response로 변경
    """
    KIPRIS API에 HTTP 요청을 보내고 기본적인 응답 및 오류를 확인합니다.

    Args:
        http_client: 사용할 httpx.AsyncClient 인스턴스.
        endpoint: 요청할 API 엔드포인트.
        params: API 요청 파라미터 (API 키 제외).
        api_key: 사용할 KIPRIS API 키.
        method: HTTP 메서드 (기본: GET).

    Returns:
        httpx.Response: 성공적인 HTTP 응답 객체.

    Raises:
        KiprisApiClientError: 네트워크 오류, 타임아웃 등 클라이언트 측 오류 발생 시.
        KiprisApiError: KIPRIS API가 명시적인 오류 코드('04' 제외)를 반환했을 때 또는 HTTP 오류 발생 시.
        KiprisApiKeyError: KIPRIS API 키 관련 오류('04') 발생 시.
        KiprisApiParsingError: KIPRIS API 응답 헤더 XML 파싱 실패 시.
    """
    request_params = params.copy()
    # API 키 파라미터 이름 결정 및 추가
    api_key_param_name = "accessKey" if endpoint.startswith("/openapi/rest/") else "ServiceKey"
    request_params[api_key_param_name] = api_key

    # 로깅 파라미터 (API 키 제외)
    log_params = {k: v for k, v in request_params.items() if k != api_key_param_name}
    logger.info(f"Sending KIPRIS API request: {method} {endpoint}", extra={"params": log_params})
    # 디버깅: 실제 사용되는 키 확인 (주의: 운영 환경에서는 민감할 수 있음)
    # logger.debug(f"Using API Key ending with: ...{api_key[-4:]}")

    try:
        response = await http_client.request(
            method,
            endpoint,
            params=request_params,
            timeout=config.HTTP_CLIENT_TIMEOUT # 설정값 사용
        )
        response.raise_for_status() # 4xx/5xx 에러 발생 시 httpx.HTTPStatusError 발생
        logger.debug(f"Received successful HTTP response ({response.status_code}) for {method} {endpoint}")

        # --- KIPRIS 헤더 오류 코드 확인 ---
        try:
            # 응답 본문이 비어있거나 XML이 아닌 경우 처리
            if not response.content:
                logger.warning(f"Empty response body received for {endpoint}")
                # 빈 응답도 성공으로 간주할지, 오류로 처리할지는 API 명세 및 정책에 따라 결정 필요
                # 여기서는 일단 성공으로 간주하고 그대로 response 반환
                return response

            xml_root = etree.fromstring(response.content)
            header = xml_root.find(".//header")
            if header is not None:
                result_code = header.findtext("resultCode")
                if result_code and result_code != '00':
                    error_msg = header.findtext("resultMsg", "KIPRIS API Error")
                    logger.error(f"KIPRIS API Error detected (Code: {result_code}): {error_msg} for {endpoint}")
                    if result_code == '04':
                        # API 키 오류는 KiprisApiKeyError 발생시켜 호출자(KiprisClient)가 처리하도록 함
                        raise KiprisApiKeyError(message=error_msg, error_code=result_code)
                    else:
                        # 다른 API 오류는 KiprisApiError 발생
                        raise KiprisApiError(message=error_msg, error_code=result_code)
            else:
                logger.warning(f"KIPRIS API response for {endpoint} is missing <header> element.")
                # 헤더가 없는 경우도 성공으로 간주할지 결정 필요
                # 여기서는 일단 성공으로 간주

        except etree.XMLSyntaxError as e:
            # 헤더 파싱 실패는 오류로 간주
            error_content = response.text[:500] # 오류 내용 일부 로깅
            msg = f"KIPRIS API 응답 헤더 XML 파싱 실패: {endpoint}"
            logger.error(f"{msg} - Response: {error_content}", exc_info=True)
            raise KiprisApiParsingError(msg) from e
        # ---------------------------------

        # 성공 시 응답 객체 그대로 반환
        return response

    except httpx.TimeoutException as e:
        msg = f"KIPRIS API 요청 시간 초과 ({config.HTTP_CLIENT_TIMEOUT}s): {endpoint}"
        logger.error(msg, exc_info=True)
        raise KiprisApiClientError(msg) from e
    except httpx.RequestError as e:
        # 네트워크 연결 오류 등
        msg = f"KIPRIS API 요청 실패 (네트워크 오류): {e}"
        logger.error(msg, exc_info=True)
        raise KiprisApiClientError(msg) from e
    except httpx.HTTPStatusError as e:
        # 4xx, 5xx 오류
        status_code = e.response.status_code
        error_content = e.response.text[:500]
        msg = f"KIPRIS API 서버 오류 응답 ({status_code}): {endpoint}"
        logger.error(f"{msg} - Response: {error_content}", exc_info=True)
        # HTTP 오류도 KiprisApiError로 변환하여 일관성 유지
        raise KiprisApiError(message=f"HTTP {status_code} 오류", error_code=str(status_code)) from e
    # KiprisApiKeyError, KiprisApiError, KiprisApiParsingError는 그대로 전달
    except (KiprisApiKeyError, KiprisApiError, KiprisApiParsingError) as e:
        raise
    except Exception as e:
        # 예상치 못한 기타 오류
        msg = f"KIPRIS API 요청 중 예상치 못한 오류 발생: {endpoint}"
        logger.critical(msg, exc_info=True)
        raise KiprisApiClientError(msg) from e