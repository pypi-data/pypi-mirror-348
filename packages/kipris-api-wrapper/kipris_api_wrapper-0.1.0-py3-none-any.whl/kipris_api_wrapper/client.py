# 생성 2025/04/28 11:56 아키텍트
# 수정 2025/04/29 12:55 코드에이전트 (Phase 2 리팩토링: 내부 함수 호출 및 재시도 로직 구현)
# 수정 2025/04/29 13:24 아키텍트 (최종 예외 처리 메시지 수정)
# 수정 2025/04/29 13:25 아키텍트 (get_api_key await 제거)
# 수정 2025/05/01 08:33 코드에이전트 (초기화 실패 및 예외 처리 로직 수정)
# 수정 2025/05/01 08:52 코드에이전트 (싱글톤 상태 관리 및 예외 처리 로직 강화)
# 수정 2025/05/15 10:35 코드에이전트 (API 키 관리 방식 변경: 외부 주입 방식으로 수정)
# 수정 2025/04/29 21:17 아키텍트 (ValueError를 KiprisApiClientError로 래핑하도록 수정)

"""
KIPRIS API 연동을 위한 메인 클라이언트 클래스
"""

import asyncio
import logging
from typing import Optional, List, Dict, Any, Type, TypeVar, Callable, Awaitable
import httpx

# 내부 모듈 임포트
from .core.auth import AuthManager
# 내부 함수 임포트 (실제 구현 파일 경로 기준)
from .trademark_get_advanced_search import _search_internal as search_advanced_trademark_internal
from .trademark_asign_product_search_info import _search_internal as search_product_info_internal
from .models import TrademarkSearchResponse, ProductCodeSearchResponse
from .exceptions import KiprisApiClientError, KiprisApiError, KiprisApiKeyError, MissingAPIKeyError
from . import config
from .utils import validate_kipris_number # 번호 유효성 검사 함수 임포트

logger = logging.getLogger(__name__)

# 싱글톤 인스턴스 및 락 (클래스 변수로 통일)
# _kipris_client_instance: Optional["KiprisClient"] = None # 전역 변수 제거
_client_lock = asyncio.Lock()
_initialization_lock = asyncio.Lock() # 초기화 전용 락 추가

T = TypeVar('T', bound='KiprisClient')

class KiprisClient:
    """
    KIPRIS Open API와 상호작용하기 위한 비동기 클라이언트 (싱글톤).

    이 클래스는 KIPRIS API 호출을 위한 표준 인터페이스를 제공하며,
    API 키 관리, HTTP 요청/응답 처리, 오류 처리 및 재시도 로직을 포함합니다.
    """
    _instance: Optional["KiprisClient"] = None
    _http_client: Optional[httpx.AsyncClient] = None
    _auth_manager: Optional[AuthManager] = None
    _initialized: bool = False # 초기화 상태 플래그
    _api_key_provider: Optional[Callable[[], Awaitable[str]]] = None # API 키 제공자 함수 저장

    def __init__(self):
        """
        직접 인스턴스화를 방지합니다. get_instance() 클래스 메서드를 사용하세요.
        """
        if self._initialized:
            return # 이미 초기화된 경우 추가 작업 방지
        raise RuntimeError("Use KiprisClient.get_instance() to get the singleton instance.")

    @classmethod
    async def _initialize(cls, api_key_provider: Callable[[], Awaitable[str]]):
        """비동기 초기화 로직 (HTTP 클라이언트 생성 등)."""
        # global _kipris_client_instance # 전역 변수 사용 제거

        async with _initialization_lock: # 초기화 락 사용
            # 이미 초기화된 경우 바로 리턴
            if cls._initialized:
                return

            logger.info("Initializing KiprisClient singleton...")
            try:
                # HTTP 클라이언트 설정 (타임아웃 등 config 사용)
                cls._http_client = httpx.AsyncClient(
                    base_url=config.KIPRIS_API_BASE_URL,
                    timeout=config.HTTP_CLIENT_TIMEOUT,
                    limits=httpx.Limits(max_connections=config.HTTP_MAX_CONNECTIONS, max_keepalive_connections=config.HTTP_MAX_KEEPALIVE_CONNECTIONS)
                )
                # API 키 제공자 함수 저장
                cls._api_key_provider = api_key_provider
                # AuthManager 인스턴스 생성 (api_key_provider 전달)
                cls._auth_manager = AuthManager(api_key_provider=api_key_provider)
                cls._initialized = True
                logger.info("KiprisClient initialized successfully.")
            except Exception as e:
                logger.critical(f"Failed to initialize KiprisClient's HTTP client: {e}", exc_info=True)
                # 초기화 실패 시 상태 초기화 (전역 변수와 클래스 변수 모두)
                cls._http_client = None
                cls._auth_manager = None
                cls._initialized = False
                cls._instance = None # 클래스 변수 _instance 초기화 추가
                cls._api_key_provider = None # API 키 제공자 함수 초기화
                # _kipris_client_instance = None # 전역 변수 제거

                # 모든 예외를 KiprisApiClientError로 래핑 (테스트에서 기대하는 메시지 사용)
                error_msg = "HTTP client initialization failed"
                raise KiprisApiClientError(error_msg) from e


    @classmethod
    async def get_instance(cls: Type[T], api_key_provider: Callable[[], Awaitable[str]]) -> T:
        """
        KiprisClient의 싱글톤 인스턴스를 반환합니다.
        첫 호출 시 비동기적으로 초기화합니다.

        Args:
            api_key_provider: API 키를 비동기적으로 제공하는 함수.
                              이 함수는 호출 시 Awaitable[str] 타입을 반환해야 합니다.

        Returns:
            KiprisClient: 초기화된 KiprisClient 인스턴스.

        Raises:
            KiprisApiClientError: 초기화 실패 시.
        """
        # global _kipris_client_instance # 전역 변수 사용 제거

        # 이미 인스턴스가 있으면 바로 반환
        if cls._instance is not None:
            return cls._instance # type: ignore  # pragma: no cover

        async with _client_lock:
            # 락 획득 후 다시 확인 (더블 체크 락킹, 클래스 변수 확인)
            if cls._instance is not None:
                return cls._instance # type: ignore

            try:
                # 클라이언트 초기화 수행 (api_key_provider 전달)
                await cls._initialize(api_key_provider)
                
                # 초기화 성공 여부 검증
                if not cls._initialized or cls._http_client is None:
                    # 초기화 실패 시 예외 발생 (테스트와 일치하는 메시지 사용)
                    logger.error("HTTP client initialization failed silently.")
                    raise KiprisApiClientError("Failed to initialize KiprisClient instance.")

                # 객체 생성 (super.__new__ 사용)
                instance = super(KiprisClient, cls).__new__(cls)
                
                # 클래스 변수에서 인스턴스 변수로 복사
                instance._http_client = cls._http_client
                instance._auth_manager = cls._auth_manager
                instance._initialized = True
                instance._api_key_provider = cls._api_key_provider
                
                # 싱글톤 인스턴스 저장 (클래스 변수에만)
                # _kipris_client_instance = instance # 전역 변수 제거
                cls._instance = instance

                logger.info("KiprisClient singleton instance created.")
                return instance
                
            except KiprisApiClientError as e:
                # 이미 KiprisApiClientError로 래핑된 예외는 그대로 전파
                logger.error(f"KiprisApiClientError during get_instance: {e}", exc_info=True)
                
                # 상태 초기화 (테스트를 위해 명시적으로 처리)
                cls._initialized = False
                cls._http_client = None
                cls._auth_manager = None
                cls._instance = None # 클래스 변수 초기화
                cls._api_key_provider = None # API 키 제공자 함수 초기화
                # _kipris_client_instance = None # 전역 변수 제거

                # 예외 다시 발생
                raise
            
            except Exception as e:
                # 다른 모든 예외는 KiprisApiClientError로 래핑
                logger.error(f"Failed to create KiprisClient instance: {e}", exc_info=True)
                
                # 상태 초기화
                cls._initialized = False
                cls._http_client = None
                cls._auth_manager = None
                cls._instance = None # 클래스 변수 초기화
                cls._api_key_provider = None # API 키 제공자 함수 초기화
                # _kipris_client_instance = None # 전역 변수 제거

                # 테스트와 일치하는 메시지로 래핑 및 전파
                error_msg = f"Failed to get KiprisClient instance: {e}"
                raise KiprisApiClientError(error_msg) from e

    @classmethod
    async def invalidate_instance(cls, reason: str = "Unknown"):
        """싱글톤 인스턴스를 무효화하고 리소스를 정리합니다 (API 키 포함)."""
        # global _kipris_client_instance # 전역 변수 사용 제거

        async with _client_lock:
            # 클래스 변수에서 인스턴스 가져오기
            instance_to_close = cls._instance

            if instance_to_close is not None:
                logger.warning(f"Invalidating KiprisClient instance. Reason: {reason}")
                
                # API 키 무효화
                if instance_to_close._auth_manager:
                    await instance_to_close._auth_manager.invalidate_api_key()
                
                # HTTP 클라이언트 닫기
                if instance_to_close._http_client:
                    await instance_to_close._http_client.aclose()
                    logger.info("KiprisClient HTTP client closed.")
                
                # 클래스 상태 초기화
                # _kipris_client_instance = None # 전역 변수 제거
                cls._instance = None
                cls._initialized = False
                cls._http_client = None
                cls._auth_manager = None
                cls._api_key_provider = None # API 키 제공자 함수 초기화

                logger.info("KiprisClient instance invalidated.")


    async def search_advanced_trademark(
        self,
        trademark_name: Optional[str] = None,
        classification_codes: Optional[List[str]] = None,
        similarity_codes: Optional[List[str]] = None,
        vienna_codes: Optional[List[str]] = None,
        applicant_name: Optional[str] = None,
        application_number: Optional[str] = None, # 출원번호 파라미터 추가
        registration_number: Optional[str] = None, # 등록번호 파라미터 추가
        rows: int = 100,
        page_no: int = 1,
        retry_count: int = 0 # 내부 재시도 횟수 추적
    ) -> TrademarkSearchResponse:
        """
        KIPRIS 상표 상세 검색 API (getAdvancedSearch)를 호출합니다.
        출원번호 또는 등록번호로도 검색 가능하며, 입력값 유효성을 검사합니다.
        API 키 오류 시 자동으로 재시도합니다.
        """
        endpoint = config.ENDPOINT_TRADEMARK_GET_ADVANCED_SEARCH
        try:
            # 0. 입력 번호 유효성 검사
            if application_number:
                validate_kipris_number(application_number, "application")
            if registration_number:
                validate_kipris_number(registration_number, "registration")

            # 1. API 키 가져오기 (await 추가)
            api_key = await self._auth_manager.get_api_key()

            # 2. HTTP 클라이언트 유효성 확인
            if self._http_client is None:
                 # 이 경우는 get_instance에서 처리되었어야 하지만 방어적으로 확인
                 logger.error("HTTP client is not available.") # pragma: no cover
                 raise KiprisApiClientError("HTTP client not initialized.") # pragma: no cover

            # 3. API별 내부 함수 호출하여 실제 작업 위임
            result: TrademarkSearchResponse = await search_advanced_trademark_internal(
                http_client=self._http_client,
                api_key=api_key,
                endpoint=endpoint,
                trademark_name=trademark_name,
                classification_codes=classification_codes,
                similarity_codes=similarity_codes,
                vienna_codes=vienna_codes,
                applicant_name=applicant_name,
                application_number=application_number, # 출원번호 전달
                registration_number=registration_number, # 등록번호 전달
                rows=rows,
                page_no=page_no,
            )
            return result

        except KiprisApiKeyError as e:
            # 4. API 키 오류 시 재시도 로직
            if retry_count < config.API_KEY_ERROR_RETRY_LIMIT:
                logger.warning(f"API Key Error detected for {endpoint}, retrying ({retry_count + 1}/{config.API_KEY_ERROR_RETRY_LIMIT})...")
                await self._auth_manager.invalidate_api_key() # 키 무효화 (await 유지)
                # 잠시 대기 (선택 사항)
                # await asyncio.sleep(1)
                # 재귀 호출로 재시도
                return await self.search_advanced_trademark(
                    trademark_name=trademark_name,
                    classification_codes=classification_codes,
                    similarity_codes=similarity_codes,
                    vienna_codes=vienna_codes,
                    applicant_name=applicant_name,
                    application_number=application_number, # 재귀 호출 시 전달
                    registration_number=registration_number, # 재귀 호출 시 전달
                    rows=rows,
                    page_no=page_no,
                    retry_count=retry_count + 1
                )
            else:
                logger.error(f"API Key Error retry limit exceeded for {endpoint}.")
                # 재시도 실패 시 MissingAPIKeyError 발생
                raise MissingAPIKeyError(f"Failed to execute {endpoint} after multiple API key retries.") from e
        except (KiprisApiClientError, KiprisApiError, MissingAPIKeyError) as e:
            # 내부 함수 또는 _request_helpers에서 발생한 다른 예상된 오류는 그대로 전달
            logger.error(f"API call failed for {endpoint}: {e}")
            raise
        except ValueError as e:
            # 번호 유효성 검사 또는 내부 파라미터 오류 시 KiprisApiClientError로 래핑
            logger.error(f"Validation or parameter error for {endpoint}: {e}")
            raise KiprisApiClientError(f"Validation or parameter error for {endpoint}: {e}") from e
        except Exception as e:
            # 예상치 못한 오류
            logger.critical(f"Unexpected error in KiprisClient.search_advanced_trademark for {endpoint}: {e}", exc_info=True)
            raise KiprisApiClientError(f"Unexpected client error processing API call for {endpoint}: {e}") from e # 메시지 수정


    async def search_product_info(
        self,
        product_keyword: str,
        rows: int = 100,
        page_no: int = 1,
        retry_count: int = 0 # 내부 재시도 횟수 추적
    ) -> ProductCodeSearchResponse:
        """
        KIPRIS 상품명 키워드 검색 API (trademarkAsignProductSearchInfo)를 호출합니다.
        API 키 오류 시 자동으로 재시도합니다.
        """
        endpoint = config.ENDPOINT_TRADEMARK_TRADEMARK_ASIGN_PRODUCT_SEARCH_INFO
        try:
            # 1. API 키 가져오기 (await 추가)
            api_key = await self._auth_manager.get_api_key()

            # 2. HTTP 클라이언트 유효성 확인
            if self._http_client is None: # pragma: no cover
                 logger.error("HTTP client is not available.") # pragma: no cover
                 raise KiprisApiClientError("HTTP client not initialized.") # pragma: no cover

            # 3. API별 내부 함수 호출
            result: ProductCodeSearchResponse = await search_product_info_internal(
                http_client=self._http_client,
                api_key=api_key,
                endpoint=endpoint,
                product_keyword=product_keyword,
                rows=rows,
                page_no=page_no,
            )
            return result

        except KiprisApiKeyError as e:
            # 4. API 키 오류 시 재시도 로직
            if retry_count < config.API_KEY_ERROR_RETRY_LIMIT:
                logger.warning(f"API Key Error detected for {endpoint}, retrying ({retry_count + 1}/{config.API_KEY_ERROR_RETRY_LIMIT})...")
                await self._auth_manager.invalidate_api_key() # await 유지
                # await asyncio.sleep(1)
                return await self.search_product_info(
                    product_keyword=product_keyword,
                    rows=rows,
                    page_no=page_no,
                    retry_count=retry_count + 1
                )
            else:
                logger.error(f"API Key Error retry limit exceeded for {endpoint}.")
                raise MissingAPIKeyError(f"Failed to execute {endpoint} after multiple API key retries.") from e
        except (KiprisApiClientError, KiprisApiError, MissingAPIKeyError) as e:
            logger.error(f"API call failed for {endpoint}: {e}")
            raise
        except Exception as e:
            logger.critical(f"Unexpected error in KiprisClient.search_product_info for {endpoint}: {e}", exc_info=True)
            raise KiprisApiClientError(f"Unexpected client error processing API call for {endpoint}: {e}") from e # 메시지 수정

    # 다른 API 메서드들도 유사한 구조로 추가될 수 있음