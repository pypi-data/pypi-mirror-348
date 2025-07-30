# 생성 2025/04/28 11:54 아키텍트
# 수정 2025/04/29 13:31 아키텍트 (HTTP 연결 상수 추가)
# 수정 2025/05/10 03:16 AI개발자 (trademarkAsignProductSearchInfo 엔드포인트 경로 수정)
# 수정 2025/05/15 10:40 코드에이전트 (GCP Secret Manager 관련 설정 제거)

"""
kipris-api-wrapper 라이브러리 설정 값 정의
"""

# KIPRIS API 기본 정보
KIPRIS_API_BASE_URL = "http://plus.kipris.or.kr"

# --- KIPRIS API 엔드포인트 경로 ---
# 상표 API
ENDPOINT_TRADEMARK_GET_ADVANCED_SEARCH = "/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch"
# 상품명 키워드 검색 API - 경로 확인 및 수정
ENDPOINT_TRADEMARK_TRADEMARK_ASIGN_PRODUCT_SEARCH_INFO = "/openapi/rest/trademarkInfoSearchService/trademarkAsignProductSearchInfo"
# ... (향후 다른 API 엔드포인트 추가) ...

# HTTP 클라이언트 설정
HTTP_CLIENT_TIMEOUT = 30.0  # 초 단위
HTTP_MAX_CONNECTIONS = 100 # 최대 동시 연결 수 (httpx 기본값)
HTTP_MAX_KEEPALIVE_CONNECTIONS = 20 # 최대 keep-alive 연결 수 (httpx 기본값)

# API 키 오류 자동 복구 설정
API_KEY_ERROR_RETRY_LIMIT = 1 # API 키 오류 시 재시도 횟수

# KIPRIS API 결과 건수 임계값 (이 값을 초과하면 KiprisTooManyResultsError 발생)
KIPRIS_RESULT_COUNT_THRESHOLD: int = 1000000

# 기타 라이브러리 관련 상수 (필요시 추가)