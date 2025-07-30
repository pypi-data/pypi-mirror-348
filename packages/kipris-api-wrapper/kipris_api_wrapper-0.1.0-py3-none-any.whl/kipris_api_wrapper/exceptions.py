# 생성 2025/04/28 11:54 아키텍트
# 수정 2025/04/28 12:28 아키텍트 (KiprisTooManyResultsError 설명 및 상속 변경)
# 수정 2025/05/10 03:25 AI개발자 (에러 코드 상수 추가)

"""
kipris-api-wrapper 라이브러리에서 사용할 사용자 정의 예외 클래스 정의
"""

from typing import Dict, Any, Optional

class KiprisApiClientError(Exception):
    """KIPRIS API 클라이언트 관련 기본 예외 (네트워크, 요청 오류, 파싱 오류 등)"""
    pass

class MissingAPIKeyError(KiprisApiClientError):
    """KIPRIS API 키를 찾을 수 없거나 로드할 수 없을 때 발생하는 예외"""
    def __init__(self, message="KIPRIS API 키를 설정하거나 로드할 수 없습니다."):
        super().__init__(message)

class KiprisApiError(KiprisApiClientError): # API 관련 오류는 클라이언트 오류의 하위로 유지
    """KIPRIS API가 명시적인 오류 코드를 반환했을 때 발생하는 예외"""
    # KIPRIS API 에러 코드 상수
    ERROR_NO_MANDATORY_PARAM = "11"      # 필수 파라미터 누락
    ERROR_INVALID_ACCESS_KEY = "101"     # 잘못된 API 키

    def __init__(self, message: str, error_code: Optional[str] = None): # error_code를 Optional로 변경하고 기본값 None 설정
        """
        Args:
            message: API가 반환한 오류 메시지 또는 관련 설명.
            error_code: KIPRIS API가 반환한 오류 코드 (예: resultCode).
        """
        self.message = message
        self.error_code = error_code

        # 에러 코드에 따른 상세 메시지 추가 (선택적)
        if error_code == self.ERROR_NO_MANDATORY_PARAM:
            self.message = f"{message} (필수 파라미터가 누락되었습니다.)"
        elif error_code == self.ERROR_INVALID_ACCESS_KEY:
             self.message = f"{message} (API 키가 유효하지 않습니다.)"

        super().__init__(self.message)

    def __str__(self) -> str:
        code_str = f"Code: {self.error_code}" if self.error_code else "Code: N/A"
        return f"KiprisApiError: {self.message} ({code_str})"

class KiprisApiKeyError(KiprisApiError):
    """KIPRIS API 키 관련 오류 ('04') 발생 시 사용되는 예외."""
    def __init__(self, message: str, error_code: str = '04'): # error_code 기본값 '04' 설정
        """
        Args:
            message: API가 반환한 오류 메시지 또는 관련 설명.
            error_code: KIPRIS API가 반환한 오류 코드 (기본값: '04').
        """
        super().__init__(message=message, error_code=error_code) # 키워드 인자 사용

class KiprisApiParsingError(KiprisApiClientError):
    """KIPRIS API 응답 XML 파싱 실패 시 발생하는 예외"""
    def __init__(self, message="KIPRIS API 응답 XML 파싱에 실패했습니다."):
        super().__init__(message)

class KiprisTooManyResultsError(KiprisApiError): # KiprisApiError 상속으로 변경
    """
    KIPRIS API가 비정상적으로 많은 결과(임계값 초과)를 반환했을 때 발생하는 예외.
    이는 KIPRIS API 자체의 버그 또는 잘못된 요청 파라미터로 인해 발생할 가능성이 높으며,
    반환된 결과는 유효하지 않은 것으로 간주해야 합니다.
    """
    def __init__(self, total_count: int, threshold: int, request_params: dict | None = None):
        """
        Args:
            total_count: API가 반환한 총 결과 수.
            threshold: 설정된 최대 허용 결과 수.
            request_params: 문제가 발생한 요청의 파라미터 (로깅용).
        """
        message = f"KIPRIS 조회 결과가 비정상적으로 많습니다 ({total_count} 건). 허용 임계값: {threshold} 건. 요청 파라미터 오류 가능성이 높습니다."
        # 이 예외는 API 동작 방식의 문제이므로 error_code는 None 또는 특정 코드로 지정 가능
        super().__init__(message=message, error_code="TooManyResults") # 키워드 인자 사용 확인
        self.total_count = total_count
        self.threshold = threshold
        self.request_params = request_params # 로깅 및 디버깅을 위해 요청 파라미터 저장

    def __str__(self) -> str:
        # 부모 클래스의 __str__을 사용하여 코드 포함
        return super().__str__()

# 필요에 따라 더 구체적인 예외 클래스 추가 가능
# 예: class KiprisTimeoutError(KiprisApiClientError): pass