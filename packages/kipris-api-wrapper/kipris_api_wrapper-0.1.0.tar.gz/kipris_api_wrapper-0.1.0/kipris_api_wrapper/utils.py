# 생성 2025/04/28 12:07 아키텍트
# 수정 2025/04/29 23:17 아키텍트 (번호 포맷팅 함수에서 권리구분코드 검증 제거)
# 수정 2025/05/11 23:31 AI개발자 (encode_special_chars_in_params 함수 추가)
# 수정 2025/04/28 23:43 아키텍트 (encode_special_chars_in_params 함수에서 '&'를 ','로 치환하도록 수정)
# 수정 2025/04/29 00:16 아키텍트 (encode_special_chars_in_params 함수 제거, httpx에 인코딩 위임)
# 수정 2025/04/29 00:19 아키텍트 (encode_special_chars_in_params 복원 및 urllib.parse.quote_plus 적용)
# 수정 2025/04/29 00:22 아키텍트 (encode_special_chars_in_params에서 quote_plus 제거, '&' 치환만 유지)
# 수정 2025/04/29 20:50 아키텍트 (등록번호 정규식 수정)

"""
kipris-api-wrapper 라이브러리 내 공통 유틸리티 함수
"""

import logging
import re
from datetime import datetime
from typing import Optional, List, Any, Dict
import urllib.parse

logger = logging.getLogger(__name__)

# --- Date Utilities 수정 ---
DATE_REGEX_YYYYMMDD = re.compile(r"^\d{8}$")
DATE_REGEX_YYYY_MM_DD = re.compile(r"^\d{4}-\d{2}-\d{2}$") # YYYY-MM-DD 형식 추가

def _validate_date_str(value: str) -> str:
    """날짜 문자열(YYYYMMDD 또는 YYYY-MM-DD)의 유효성을 검사하고 YYYYMMDD 형식으로 반환"""
    stripped_value = value.strip()
    date_to_parse = stripped_value
    yyyymmdd_format = "" # YYYYMMDD 형식 저장 변수

    if DATE_REGEX_YYYYMMDD.match(stripped_value):
        format_str = '%Y%m%d'
        yyyymmdd_format = stripped_value
    elif DATE_REGEX_YYYY_MM_DD.match(stripped_value):
        format_str = '%Y-%m-%d'
        # YYYY-MM-DD 형식을 YYYYMMDD로 변환
        yyyymmdd_format = stripped_value.replace("-", "")
    else:
        raise ValueError(f"Invalid date format: '{value}'. Expected YYYYMMDD or YYYY-MM-DD.")

    try:
        # 날짜 유효성 검사
        datetime.strptime(date_to_parse, format_str)
        return yyyymmdd_format # 검증 후 YYYYMMDD 형식 반환
    except ValueError:
        logger.warning(f"Invalid date value: {date_to_parse}")
        raise ValueError(f"Invalid date value: {date_to_parse}")

def format_date_iso(value: Any) -> Optional[str]:
    """
    날짜 형식의 입력(YYYYMMDD 또는 YYYY-MM-DD 문자열)을 검증하고
    YYYY-MM-DD 형식으로 변환하여 반환합니다. 유효하지 않으면 ValueError 발생.
    """
    if value is None or value == "" or str(value).strip() == "":
        return None
    if isinstance(value, str):
        try:
            yyyymmdd_str = _validate_date_str(value) # 내부 헬퍼 사용 (YYYYMMDD 반환)
            return f"{yyyymmdd_str[:4]}-{yyyymmdd_str[4:6]}-{yyyymmdd_str[6:]}"
        except ValueError as e:
            raise e # ValueError 다시 발생
    raise ValueError(f"Unexpected type for date formatting: {type(value)}")


# --- Parsing Utilities 수정 ---
def parse_separated_list(value: Any, separators: str = r'[;,\s]+') -> Optional[List[str]]:
    """
    지정된 구분자(기본값: 세미콜론, 콤마, 공백)로 구분된 문자열을
    정렬된 문자열 리스트로 파싱합니다. 입력이 리스트인 경우에도 처리합니다.
    리스트 내 None 값과 빈 문자열은 필터링합니다.
    """
    if isinstance(value, str):
        items = [item.strip() for item in re.split(separators, value) if item.strip()]
        return sorted(items) if items else None
    elif isinstance(value, list):
         # None 값과 빈 문자열 필터링 수정
         items = [str(item).strip() for item in value if item is not None and str(item).strip()]
         return sorted(items) if items else None
    elif value is None:
        return None
    else:
        logger.warning(f"Cannot parse separated list from type {type(value)}. Value: {value}")
        return None

# --- KIPRIS Number Utilities ---
# 정규 표현식 정의
PATTERN1_REGEX = re.compile(r"^(\d{2})(\d{4})(\d{7})$") # XXYYYYNNNNNNN (13자리) - 출원번호
PATTERN2_REGEX = re.compile(r"^(\d{2})(\d{7})$")       # XXNNNNNNN (9자리) - 등록번호 (API 응답 아님)
PATTERN_REG_API_RESPONSE = re.compile(r"^(\d{2})(\d{7})0000$") # XXNNNNNNN0000 (13자리) - 등록번호 API 응답

# 번호 유효성 검사 패턴 (사용자 입력 형식)
APP_NUM_REGEX = re.compile(r"^40-\d{4}-\d{7}$") # 출원번호: 40-YYYY-NNNNNNN
REG_NUM_REGEX = re.compile(r"^40-\d{7}$")       # 등록번호: 40-NNNNNNN (하이픈 뒤 4자리 제거)

def prepare_api_number_param(number_str: Optional[str], number_type: str) -> Optional[str]:
    """
    API 요청 파라미터에 사용될 번호 문자열을 준비합니다.
    하이픈을 제거하고, 등록번호의 경우 뒤에 '0000'을 추가합니다.

    Args:
        number_str: 하이픈을 포함할 수 있는 번호 문자열.
        number_type: 번호 유형 ('application' 또는 'registration').

    Returns:
        API 파라미터 형식에 맞게 처리된 번호 문자열.
        입력이 None이거나 빈 문자열이면 None.

    Raises:
        ValueError: number_type이 유효하지 않은 경우.
    """
    if number_str is None or not str(number_str).strip():
        return None

    cleaned_number = str(number_str).replace("-", "").strip()

    if number_type == 'application':
        # 출원번호는 하이픈만 제거
        return cleaned_number
    elif number_type == 'registration':
        # 등록번호는 하이픈 제거 후 '0000' 추가
        # 입력 형식은 40-NNNNNNN 또는 40NNNNNNN 가정
        if len(cleaned_number) == 9 and cleaned_number.startswith("40"): # 40NNNNNNN
             return cleaned_number + "0000"
        else:
             # 예상치 못한 형식의 등록번호 입력 처리
             logger.warning(f"Unexpected registration number format for API param preparation: '{number_str}'. Expected '40-NNNNNNN' or '40NNNNNNN'. Returning cleaned number without placeholder.")
             return cleaned_number # 일단 하이픈 제거된 것만 반환 (오류 대신 경고)
    else:
        raise ValueError(f"Invalid number_type: '{number_type}'. Expected 'application' or 'registration'.")


def validate_kipris_number(number_str: Optional[str], number_type: str) -> Optional[str]:
    """
    사용자 입력 KIPRIS 번호 문자열의 유효성을 검사합니다 (하이픈 포함 형식).
    등록번호는 '40-NNNNNNN' 형식만 유효합니다.

    Args:
        number_str: 검사할 번호 문자열 (하이픈 포함).
        number_type: 번호 유형 ('application' 또는 'registration').

    Returns:
        유효한 경우 입력 number_str을 그대로 반환.
        입력이 None이거나 빈 문자열이면 None 반환.

    Raises:
        ValueError: 번호 형식이 유효하지 않은 경우.
    """
    if number_str is None or not str(number_str).strip():
        return None

    str_value = str(number_str).strip()

    if number_type == 'application':
        expected_pattern = "40-YYYY-NNNNNNN"
        regex = APP_NUM_REGEX
    elif number_type == 'registration':
        expected_pattern = "40-NNNNNNN" # 등록번호 형식 (사용자 입력)
        regex = REG_NUM_REGEX
    else:
        raise ValueError(f"Invalid number_type: '{number_type}'. Expected 'application' or 'registration'.")

    if not regex.match(str_value):
        raise ValueError(f"Invalid {number_type} number format: '{str_value}'. Expected format: {expected_pattern}")

    return str_value # 유효하면 원본 문자열 반환

def format_kipris_number_2x4y7d(value: Any) -> Optional[str]:
    """
    KIPRIS API 응답의 13자리 출원/공고번호(XXYYYYNNNNNNN)를
    표준 형식(XX-YYYY-NNNNNNN)으로 변환합니다.
    다른 형식의 입력은 원본 문자열을 반환합니다.

    Args:
        value: 포매팅할 번호 문자열 또는 숫자.

    Returns:
        포매팅된 번호 문자열(XX-YYYY-NNNNNNN) 또는 원본 문자열. None 입력 시 None 반환.
    """
    if value is None:
        return None

    original_str_value: Optional[str] = None
    try:
        original_str_value = str(value).strip()
        if not original_str_value:
            return None

        num_str = original_str_value

        # 출원번호 패턴 (13자리, XXYYYYNNNNNNN) 검사
        match_p1 = PATTERN1_REGEX.match(num_str)
        if match_p1:
            right_code = match_p1.group(1)
            year = match_p1.group(2)
            serial = match_p1.group(3)
            return f"{right_code}-{year}-{serial}"
        else:
            # 패턴 불일치 시 원본 반환
            # logger.debug(f"Input '{num_str}' does not match 2x4y7d pattern. Returning original.")
            return num_str

    except Exception as e:
        logger.error(f"Error formatting KIPRIS 2x4y7d number '{value}': {e}", exc_info=True)
        return original_str_value


def format_kipris_number_2x7d(value: Any) -> Optional[str]:
    """
    KIPRIS API 응답의 등록번호 관련 문자열을 표준 형식(XX-NNNNNNN)으로 변환합니다.
    - 13자리 API 응답 (XXNNNNNNN0000) -> XX-NNNNNNN
    - 9자리 등록번호 (XXNNNNNNN) -> XX-NNNNNNN
    다른 형식의 입력은 원본 문자열을 반환합니다.

    Args:
        value: 포매팅할 번호 문자열 또는 숫자.

    Returns:
        포매팅된 번호 문자열(XX-NNNNNNN) 또는 원본 문자열. None 입력 시 None 반환.
    """
    if value is None:
        return None

    original_str_value: Optional[str] = None
    try:
        original_str_value = str(value).strip()
        if not original_str_value:
            return None

        num_str = original_str_value

        # 1. 등록번호 API 응답 패턴 (13자리, XXNNNNNNN0000) 검사
        match_reg_api = PATTERN_REG_API_RESPONSE.match(num_str)
        if match_reg_api:
            right_code = match_reg_api.group(1)
            serial = match_reg_api.group(2)
            return f"{right_code}-{serial}"

        # 2. 9자리 등록번호 패턴 (XXNNNNNNN) 검사
        match_p2 = PATTERN2_REGEX.match(num_str)
        if match_p2:
            right_code = match_p2.group(1)
            serial = match_p2.group(2)
            logger.debug(f"Formatting 9-digit number '{num_str}' to '{right_code}-{serial}'.")
            return f"{right_code}-{serial}"

        # 어떤 등록번호 패턴에도 맞지 않는 경우
        # logger.debug(f"Input '{num_str}' does not match known registration number patterns for formatting. Returning original.")
        return num_str

    except Exception as e:
        logger.error(f"Error formatting KIPRIS 2x7d number '{value}': {e}", exc_info=True)
        return original_str_value
# --- URL Parameter 처리 유틸리티 ---
def encode_special_chars_in_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    API 요청 파라미터 값 중 KIPRIS API에서 특별하게 처리하는 '&' 문자를 ','로 치환합니다.
    다른 URL 인코딩은 httpx 라이브러리에 위임합니다.

    Args:
        params: 요청 파라미터 딕셔너리

    Returns:
        처리된 파라미터 딕셔너리
    """
    if not params:
        return {}

    result = {}
    for key, value in params.items():
        if isinstance(value, str):
            # '&' 문자가 포함된 경우 ','로 치환 (KIPRIS API 특수 요구사항)
            if '&' in value:
                new_value = value.replace('&', ',')
                logger.debug(f"Replacing '&' with ',' in parameter '{key}': '{value}' -> '{new_value}'")
                result[key] = new_value
            else:
                result[key] = value
        else:
            # 문자열이 아닌 값은 그대로 유지
            result[key] = value

    return result
