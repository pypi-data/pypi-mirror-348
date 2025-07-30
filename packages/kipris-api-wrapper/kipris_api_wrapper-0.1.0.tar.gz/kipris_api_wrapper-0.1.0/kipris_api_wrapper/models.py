# 생성 2025/04/28 11:54 아키텍트
# 수정 2025/04/28 12:08 아키텍트 (utils 함수 사용하도록 validator 수정)
# 수정 2025/05/10 03:15 AI개발자 (ProductCodeInfo 모델 필드 확장)
# 수정 2025/05/10 03:36 AI개발자 (ProductCodeInfo 모델 필드명 표준화)
# 수정 2025/05/10 04:22 AI개발자 (ProductCodeInfo 필드명 변경)
# 수정 2025/04/29 23:13 아키텍트 (번호 포맷팅 validator 분리: format_app_pub_numbers, format_reg_number)
# 수정 2025/04/29 22:41 아키텍트 (리스트 구분자를 '|'만 사용하도록 수정)

"""
kipris-api-wrapper 라이브러리에서 사용할 표준 Pydantic 데이터 모델 정의
KIPRIS API 응답을 파싱하고 내부적으로 사용하기 위한 구조
"""

import logging
from typing import Optional, List, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

# 내부 유틸리티 임포트
from . import utils

logger = logging.getLogger(__name__)

class TrademarkItem(BaseModel):
    """
    KIPRIS 상표 검색 결과의 개별 항목 표준 모델 (getAdvancedSearch)
    필드명은 내부 표준인 snake_case 사용
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    index_no: Optional[str] = Field(None, description="Index Number")
    application_number: Optional[str] = Field(None, description="출원번호 (XX-YYYY-ZZZZZZZ)")
    application_date: Optional[str] = Field(None, description="출원일자 (YYYY-MM-DD)")
    publication_number: Optional[str] = Field(None, description="공고번호 (XX-YYYY-ZZZZZZZ)") # Validator가 표준 형식으로 변환
    publication_date: Optional[str] = Field(None, description="공고일자 (YYYY-MM-DD)")
    registration_number: Optional[str] = Field(None, description="등록번호 (XX-ZZZZZZZ)")
    registration_date: Optional[str] = Field(None, description="등록일자 (YYYY-MM-DD)")
    applicant_name: Optional[List[str]] = Field(None, description="출원인명 리스트 (';' 또는 '|' 구분자 포함될 수 있음)")
    agent_name: Optional[List[str]] = Field(None, description="대리인명 리스트 (';' 또는 '|' 구분자 포함될 수 있음)")
    vienna_code: Optional[List[str]] = Field(None, description="비엔나 코드 리스트")
    trademark_name: Optional[str] = Field(None, description="상표 명칭 (title)")
    image_url: Optional[str] = Field(None, description="이미지 URL (bigDrawing)")
    classification_code: Optional[List[str]] = Field(None, description="상품 분류 코드(NICE) 리스트")
    application_status: Optional[str] = Field(None, description="상표 상태 (예: 등록, 거절, 출원)")
    registration_privilege_name: Optional[List[str]] = Field(None, description="등록권리자명 리스트 (';' 또는 '|' 구분자 포함될 수 있음)")

    # --- Validators ---

    @field_validator('application_number', 'publication_number', mode='before')
    @classmethod
    def format_app_pub_numbers(cls, value: Any) -> Optional[str]:
        """출원번호 및 공고번호 필드를 표준 형식(XX-YYYY-NNNNNNN)으로 변환"""
        if value is None:
            return None
        try:
            # utils.format_kipris_number_2x4y7d는 유효하지 않으면 원본 반환
            return utils.format_kipris_number_2x4y7d(value)
        except Exception as e:
            logger.warning(f"Error formatting application/publication number: {e}. Returning original value: {value}", exc_info=True)
            return str(value)

    @field_validator('registration_number', mode='before')
    @classmethod
    def format_reg_number(cls, value: Any) -> Optional[str]:
        """등록번호 필드를 표준 형식(XX-NNNNNNN)으로 변환"""
        if value is None:
            return None
        try:
            # utils.format_kipris_number_2x7d는 유효하지 않으면 원본 반환
            return utils.format_kipris_number_2x7d(value)
        except Exception as e:
            logger.warning(f"Error formatting registration number: {e}. Returning original value: {value}", exc_info=True)
            return str(value)
    @field_validator('application_date', 'publication_date', 'registration_date', mode='before')
    @classmethod
    def format_dates_iso(cls, value: Any) -> Optional[str]:
        """날짜 필드를 YYYY-MM-DD 형식으로 변환 (utils 사용)"""
        try:
            # utils.format_date_iso는 유효하지 않은 경우 ValueError 발생
            return utils.format_date_iso(value)
        except ValueError as e:
            # ValueError를 다시 발생시켜 Pydantic이 처리하도록 함
            raise e

    @field_validator('classification_code', 'vienna_code', 'applicant_name', 'agent_name', 'registration_privilege_name', mode='before')
    @classmethod
    def parse_list_fields(cls, value: Any) -> Optional[List[str]]:
        """세미콜론(;) 또는 파이프(|) 등으로 구분된 문자열을 리스트로 파싱 (utils 사용)"""
        # 구분자에 '|' 추가
        return utils.parse_separated_list(value, separators=r'[|]') # 구분자를 '|'만 사용

class TrademarkSearchResponse(BaseModel):
    """KIPRIS 상표 검색 API 응답 표준 모델"""
    model_config = ConfigDict(str_strip_whitespace=True)

    total_count: int = Field(..., description="총 검색 결과 수")
    items: List[TrademarkItem] = Field(default_factory=list, description="검색된 상표 목록")

# --- 다른 API 응답 모델 (향후 추가) ---

class ProductCodeInfo(BaseModel):
    """상품명 키워드 검색 결과 항목 모델 (trademarkAsignProductSearchInfo)"""
    model_config = ConfigDict(str_strip_whitespace=True)

    product_name: Optional[str] = Field(None, description="상품/서비스 명칭")
    classification_code: Optional[str] = Field(None, description="NICE 분류 코드")
    similarity_codes: Optional[List[str]] = Field(None, description="유사군 코드 리스트")
    product_name_en: Optional[str] = Field(None, description="상품/서비스 영문 명칭")
    product_description: Optional[str] = Field(None, description="상품/서비스 설명 정보")
    version: Optional[str] = Field(None, description="버전 정보")
    product_number: Optional[str] = Field(None, description="상품 번호")
    is_main: Optional[bool] = Field(None, description="주요 상품 여부")

    @field_validator('similarity_codes', mode='before')
    @classmethod
    def parse_similarity_code_list(cls, value: Any) -> Optional[List[str]]:
        """유사군 코드 문자열을 리스트로 파싱 (utils 사용)"""
        # 유사군 코드는 공백 또는 콤마 등으로 구분될 수 있음
        return utils.parse_separated_list(value)

class ProductCodeSearchResponse(BaseModel):
    """상품명 키워드 검색 API 응답 모델"""
    model_config = ConfigDict(str_strip_whitespace=True)

    total_count: int = Field(..., description="총 검색 결과 수")
    results: List[ProductCodeInfo] = Field(default_factory=list, description="검색된 상품/서비스 목록")

# ... Vienna 코드 검색, 상세 정보 조회 등 다른 모델 추가 ...