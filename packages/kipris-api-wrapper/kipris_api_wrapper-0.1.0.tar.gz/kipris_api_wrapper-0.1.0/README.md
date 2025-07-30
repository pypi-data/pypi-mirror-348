# KIPRIS API Wrapper (`kipris-api-wrapper`)

<!-- 생성 2025/04/29 12:47 코드에이전트 -->
<!-- 수정 2025/05/17 18:22 Architect -->

## 개요

이 라이브러리는 KIPRIS Open API와의 통신을 추상화하고 표준화된 인터페이스를 제공하여, KIPRIS API 기능을 파이썬 애플리케이션에서 쉽고 안정적으로 사용할 수 있도록 돕습니다.

**현재 릴리스 버전: v0.1.3** (pyproject.toml 기준)

**주요 변경 사항 (2025년 5월 17일):**
*   패키지 관리 도구가 Poetry에서 `uv`로 전환되었습니다.
*   Python 3.12 환경에서 모든 테스트(282개)를 통과했으며, 코드 커버리지 96%를 달성했습니다.

주요 기능은 다음과 같습니다:

*   **클래스 기반 인터페이스:** `KiprisClient` 클래스를 통해 모든 API 기능에 접근합니다.
*   **비동기 지원:** `asyncio` 및 `httpx`를 기반으로 비동기적으로 작동합니다.
*   **유연한 API 키 관리:** 라이브러리 사용자가 제공하는 함수를 통해 API 키를 로드하고, 키 오류 발생 시 자동으로 복구를 시도합니다. (특정 환경 종속성 없음)
*   **표준 데이터 모델:** KIPRIS API의 복잡한 XML 응답을 Pydantic 모델로 변환하여 제공합니다.
*   **오류 처리:** 네트워크 오류, API 자체 오류 등을 표준화된 예외 클래스로 처리합니다.

## 설치

PyPI에서 `uv`를 사용하여 설치합니다.

```bash
uv pip install kipris-api-wrapper
```

**선택적 의존성 설치:**

특정 기능을 사용하기 위해 추가 의존성을 설치할 수 있습니다.

*   GCP Secret Manager를 사용하여 API 키를 로드하는 경우:
    ```bash
    uv pip install "kipris-api-wrapper[gcp]"
    ```
*   로컬 개발 시 `.env` 파일에서 환경 변수를 로드하는 경우:
    ```bash
    uv pip install "kipris-api-wrapper[local]"
    ```

**개발/테스트 시 로컬 설치:**

프로젝트를 클론한 후, `packages/kipris_api_wrapper` 디렉토리에서 다음 명령을 실행하여 편집 가능한 모드로 설치할 수 있습니다.

```bash
uv pip install -e .
```

*(참고: Git 저장소에서 직접 설치하는 예시는 PyPI 배포 후에는 일반 사용자에게는 덜 필요하므로, 개발자용 고급 설치 방법으로 남기거나 제거할 수 있습니다. 우선은 유지하겠습니다.)*

```bash
# Git 저장소에서 직접 설치 (최신 개발 버전 등)
uv pip install git+https://github.com/patentsong/songohip.git#subdirectory=packages/kipris_api_wrapper
```

## 설정: API 키 제공 함수 주입 (필수)

이 라이브러리는 API 키를 직접 관리하지 않습니다. 대신, **API 키를 반환하는 비동기 함수(Provider)를 구현하여 `KiprisClient` 초기화 시 주입**해야 합니다. 이는 라이브러리가 특정 환경(예: GCP Secret Manager, 환경 변수)에 종속되지 않도록 하기 위함입니다.

**API 키 제공 함수 요구사항:**

*   비동기 함수 (`async def`)여야 합니다.
*   호출 시 유효한 KIPRIS API 키 문자열을 반환해야 합니다.
*   키 로드 실패 시 `kipris_api_wrapper.exceptions.MissingAPIKeyError` 또는 하위 호환되는 예외를 발생시켜야 합니다.
*   라이브러리는 API 키 오류 발생 시 이 함수를 다시 호출하여 새로운 키를 얻으려고 시도하므로, 필요시 최신 키를 반환하도록 구현해야 합니다. (예: Secret Manager에서 키 갱신)
*   **실제 애플리케이션(예: `kipris_trademark_mcp` 서버)에서는 이 `api_key_provider` 함수 내에서 환경 변수(`os.environ.get("KIPRIS_API_KEY")`)를 읽거나, GCP Secret Manager와 같은 보안 저장소에서 API 키를 가져오는 로직을 구현하는 것을 강력히 권장합니다.**

**예시: 다양한 환경에서의 API 키 제공 함수 구현**

```python
import os
import asyncio
from kipris_api_wrapper.exceptions import MissingAPIKeyError

# 예시 1: 환경 변수에서 로드
async def load_key_from_env():
    api_key = os.environ.get("KIPRIS_API_KEY")
    if not api_key:
        raise MissingAPIKeyError("KIPRIS_API_KEY environment variable not set.")
    print("Loaded API key from environment variable.") # 실제 사용 시 로깅 등으로 대체
    return api_key

# 예시 2: 파일에서 로드
async def load_key_from_file(filepath="path/to/your/api_key.txt"):
    try:
        with open(filepath, 'r') as f:
            api_key = f.read().strip()
        if not api_key:
            raise MissingAPIKeyError(f"API key file '{filepath}' is empty.")
        print(f"Loaded API key from file: {filepath}")
        return api_key
    except FileNotFoundError:
        raise MissingAPIKeyError(f"API key file not found: {filepath}")
    except Exception as e:
        raise MissingAPIKeyError(f"Failed to read API key from file: {e}")

# 예시 3: GCP Secret Manager에서 로드 (kipris-api-wrapper[gcp] 설치 필요)
# 이 함수는 라이브러리 사용자의 프로젝트에 위치해야 합니다.
async def load_key_from_gcp_secret_manager():
    try:
        from google.cloud import secretmanager
        # 필요한 설정값 (환경 변수, 설정 파일 등에서 로드)
        gcp_project_id = os.environ.get("GCP_PROJECT_ID")
        secret_id = os.environ.get("KIPRIS_API_SECRET_ID")
        secret_version = os.environ.get("KIPRIS_API_SECRET_VERSION", "latest")

        if not all([gcp_project_id, secret_id]):
             raise MissingAPIKeyError("GCP_PROJECT_ID or KIPRIS_API_SECRET_ID not configured.")

        client = secretmanager.SecretManagerServiceClient() # 동기 클라이언트
        secret_name = f"projects/{gcp_project_id}/secrets/{secret_id}/versions/{secret_version}"

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None, client.access_secret_version, {"name": secret_name}
        )
        api_key = response.payload.data.decode("UTF-8").strip()
        if not api_key:
            raise MissingAPIKeyError("Fetched empty API key from Secret Manager.")
        print("Loaded API key from GCP Secret Manager.")
        return api_key
    except ImportError:
         raise ImportError("Please install 'kipris-api-wrapper[gcp]' to use GCP Secret Manager.")
    except Exception as e:
        raise MissingAPIKeyError(f"Failed to load API key from GCP Secret Manager: {e}")

```

## 기본 사용법

```python
import asyncio
import os # API 키 제공 함수 예시를 위해 추가
from kipris_api_wrapper import KiprisClient, TrademarkSearchResponse, ProductCodeSearchResponse
from kipris_api_wrapper.exceptions import KiprisApiClientError, KiprisApiError, MissingAPIKeyError

# --- 사용할 API 키 제공 함수 선택 ---
# from your_project.config import load_key_from_env as api_key_provider # 예시
# from your_project.secrets import load_key_from_gcp_secret_manager as api_key_provider # 예시

# 여기서는 환경 변수 사용 예시
async def load_key_from_env():
    api_key = os.environ.get("KIPRIS_API_KEY")
    if not api_key:
        raise MissingAPIKeyError("KIPRIS_API_KEY environment variable not set.")
    print("Loaded API key from environment variable.")
    return api_key

api_key_provider = load_key_from_env
# ---------------------------------

async def main():
    try:
        # 싱글톤 클라이언트 인스턴스 가져오기 (API 키 제공 함수 주입 필수)
        client = await KiprisClient.get_instance(api_key_provider=api_key_provider)

        # 예시 1: 상표 상세 검색 (getAdvancedSearch)
        print("Searching for trademark 'ExampleBrand'...")
        trademark_results: TrademarkSearchResponse = await client.search_advanced_trademark(
            trademark_name="ExampleBrand",
            rows=10,
            page_no=1
        )
        print(f"Found {trademark_results.total_count} trademarks.")
        for item in trademark_results.items:
            print(f"- App No: {item.application_number}, Name: {item.trademark_name}, Status: {item.application_status}")

        print("\n" + "="*20 + "\n")

        # 예시 2: 상품명 키워드 검색 (trademarkAsignProductSearchInfo)
        print("Searching for product keyword 'computer'...")
        product_results: ProductCodeSearchResponse = await client.search_product_info(
            product_keyword="computer",
            rows=5
        )
        print(f"Found {product_results.total_count} product codes.")
        for result in product_results.results:
            print(f"- Product: {result.product_name}, Class: {result.classification_code}, Similarity: {result.similarity_codes}")

    except MissingAPIKeyError as e:
        print(f"Error: Failed to obtain KIPRIS API Key. Details: {e}")
    except KiprisApiError as e:
        print(f"Error: KIPRIS API returned an error. Code: {e.error_code}, Message: {e.message}")
    except KiprisApiClientError as e:
        print(f"Error: Failed to communicate with KIPRIS API. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 애플리케이션 종료 시 클라이언트 리소스 정리 (선택 사항이지만 권장)
        await KiprisClient.invalidate_instance("Application shutting down")


if __name__ == "__main__":
    # 로깅 설정 (선택 사항)
    # import logging
    # logging.basicConfig(level=logging.INFO)

    # API 키 제공 함수가 환경 변수를 사용한다고 가정
    # 실제 실행 전 `export KIPRIS_API_KEY='your_actual_api_key'` 필요
    if not os.environ.get("KIPRIS_API_KEY"):
        print("Error: KIPRIS_API_KEY environment variable is not set.")
        print("Please set it before running the example: export KIPRIS_API_KEY='your_key'")
    else:
        asyncio.run(main())

```

## 예외 처리

라이브러리는 다음과 같은 주요 예외를 발생시킬 수 있습니다.

*   `kipris_api_wrapper.MissingAPIKeyError`: API 키 제공 함수가 키를 반환하지 못하거나 로드에 실패한 경우.
*   `kipris_api_wrapper.KiprisApiKeyError`: 제공된 API 키가 KIPRIS 서버에서 유효하지 않다고 응답한 경우 (라이브러리가 자동으로 재시도 후에도 실패 시 `MissingAPIKeyError`로 변환될 수 있음).
*   `kipris_api_wrapper.KiprisApiError`: KIPRIS API가 키 오류 외 다른 오류 코드를 반환한 경우 또는 HTTP 오류(4xx, 5xx) 발생 시. `error_code`와 `message` 속성을 확인하세요.
*   `kipris_api_wrapper.KiprisTooManyResultsError`: API 조회 결과가 비정상적으로 많은 경우 (설정된 임계값 초과). 요청 파라미터 오류 가능성이 높습니다.
*   `kipris_api_wrapper.KiprisApiParsingError`: API 응답 XML 파싱에 실패한 경우.
*   `kipris_api_wrapper.KiprisApiClientError`: 네트워크 연결 실패, 타임아웃 등 라이브러리 내부 또는 통신 중 오류 발생 시.

## 상세 명세 및 개발 계획

*   [라이브러리 상세 명세](./docs/spec.md)
*   [개발 태스크 목록](./docs/tasks.md)

## 기여

(기여 방법에 대한 안내 추가 예정)

## 라이선스

MIT License (pyproject.toml 참조)