# 생성 2025/04/28 11:56 아키텍트
# 수정 2025/04/29 12:37 코드에이전트 (공개 인터페이스 정리)
# 수정 2025/04/27 15:02 AI개발자 (테스트 커버리지 개선용 export 추가) - 이전 수정 내역 유지

"""
KIPRIS API Python 래퍼 패키지

특허 및 상표 정보를 검색하기 위한 KIPRIS 오픈 API 래퍼 모듈입니다.
"""

__version__ = "0.1.0"

# KiprisClient 클래스 자체를 임포트
from .client import KiprisClient
# 공개 예외 클래스 임포트
from .exceptions import (
    KiprisApiClientError,
    MissingAPIKeyError,
    KiprisApiError,
    KiprisApiParsingError, # KiprisClient에서 직접 발생시키지는 않지만, 내부 함수에서 발생 가능성 있음
    KiprisTooManyResultsError,
    KiprisApiKeyError, # API 키 오류 예외 추가
)
# 공개 모델 클래스 임포트
from .models import (
    TrademarkItem,
    TrademarkSearchResponse,
    ProductCodeInfo,
    ProductCodeSearchResponse,
    # ... 향후 추가될 공개 모델 ...
)

# API 래핑 함수 직접 임포트 제거 (KiprisClient 메서드를 통해 접근)
# from .trademark_get_advanced_search import search_advanced_trademark
# from .trademark_asign_product_search_info import search_product_info, parse_product_item
# ... 다른 API 래핑 함수 임포트 제거 ...

__all__ = [
    # Client
    "KiprisClient", # 클래스 자체만 노출

    # Exceptions (공개 인터페이스로 간주되는 예외)
    "KiprisApiClientError",
    "MissingAPIKeyError",
    "KiprisApiError",
    "KiprisApiParsingError",
    "KiprisTooManyResultsError",
    "KiprisApiKeyError",

    # Models (공개 인터페이스로 간주되는 모델)
    "TrademarkItem",
    "TrademarkSearchResponse",
    "ProductCodeInfo",
    "ProductCodeSearchResponse",
    # ... 향후 추가될 공개 모델 이름 ...
]