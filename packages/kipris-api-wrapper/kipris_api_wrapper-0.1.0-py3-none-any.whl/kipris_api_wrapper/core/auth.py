# 생성 2025/04/29 12:35 코드에이전트
# 수정 2025/04/29 12:35 코드에이전트
# 수정 2025/05/15 10:30 코드에이전트 (API 키 관리 방식 변경: 외부 주입 방식으로 수정)

"""
KIPRIS API 인증 및 키 관리 모듈.
API 키를 외부에서 비동기 함수 형태로 주입받아 관리합니다.
"""

import asyncio
import logging
from typing import Optional, Callable, Awaitable

# 내부 모듈 임포트 - 경로 주의
from ..exceptions import MissingAPIKeyError

logger = logging.getLogger(__name__)

class AuthManager:
    """
    API 키 로딩, 저장, 갱신 로직을 관리하는 클래스.
    """
    _api_key: Optional[str] = None
    _lock = asyncio.Lock() # 동시성 제어를 위한 Lock

    def __init__(self, api_key_provider: Callable[[], Awaitable[str]]):
        """
        AuthManager 초기화.

        Args:
            api_key_provider: API 키를 비동기적으로 반환하는 함수.
                             이 함수는 호출 시 Awaitable[str] 타입을 반환해야 합니다.
        """
        self._api_key_provider = api_key_provider

    async def get_api_key(self) -> str:
        """
        저장된 API 키를 반환하거나, 없으면 api_key_provider 함수를 호출하여 로드하여 반환합니다.

        Returns:
            str: KIPRIS API 키.

        Raises:
            MissingAPIKeyError: API 키를 로드할 수 없는 경우.
        """
        # 이미 키가 로드되었으면 바로 반환
        if self._api_key:
            return self._api_key

        # 키가 없으면 Lock을 잡고 로드 시도
        async with self._lock:
            # Lock 획득 후 다시 한번 확인 (더블 체크 락)
            if self._api_key is None:
                logger.info("API key not found in memory, attempting to load from provided api_key_provider...")
                try:
                    api_key = await self._api_key_provider()
                    if not api_key:
                        raise MissingAPIKeyError("API key provider returned an empty key.")
                    
                    self._api_key = api_key
                    logger.info("API key loaded successfully.")
                except Exception as e:
                    logger.critical(f"API 키를 가져오는 데 실패했습니다: {e}", exc_info=True)
                    # 여기서 발생하는 모든 예외는 MissingAPIKeyError로 변환하여 일관성 유지
                    raise MissingAPIKeyError(f"API 키 획득 실패: {e}") from e
            
            return self._api_key

    async def invalidate_api_key(self):
        """
        현재 메모리에 저장된 API 키를 무효화합니다.
        다음 get_api_key 호출 시 api_key_provider에서 새로 로드됩니다.
        """
        async with self._lock:
            if self._api_key is not None:
                logger.warning("Invalidating stored API key.")
                self._api_key = None
            else:
                logger.info("API key was already invalidated.")

# 싱글톤 인스턴스 (필요시 KiprisClient 내부에서 관리해도 무방)
# auth_manager = AuthManager()