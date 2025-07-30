<!-- 생성 2025/04/29 17:51 아키텍트 -->
<!-- 수정 2025/05/18 11:58 Architect -->

# KIPRIS Trademark MCP Server (`kipris-trademark-mcp`)

## 1. 개요

이 MCP(Model Context Protocol) 서버는 KIPRIS Open API의 상표 관련 기능을 활용하여, AI 에이전트가 상표 정보를 검색하고 상품 분류 코드를 조회하는 등 상표 분석에 필요한 핵심 도구들을 제공합니다.

**현재 릴리스 버전: v0.1.0 (PyPI 최초 배포)**

**주요 특징:**

*   **KIPRIS API 연동:** `kipris-api-wrapper` 라이브러리를 사용하여 KIPRIS Open API와 안정적으로 통신합니다.
*   **표준화된 도구:** AI 에이전트가 쉽게 사용할 수 있도록 표준화된 MCP 도구 인터페이스를 제공합니다.
*   **비동기 처리:** `fastmcp` 프레임워크와 `asyncio`를 기반으로 비동기적으로 작동하여 효율적인 처리가 가능합니다.
*   **Stdio 통신:** 표준 입출력(Stdio)을 통해 MCP 클라이언트와 통신합니다.

## 2. 설치

PyPI에서 `uv`를 사용하여 설치합니다.

```bash
uv pip install kipris-trademark-mcp
```
이 패키지는 `kipris-api-wrapper` (PyPI) 및 `fastmcp` (PyPI) 등의 의존성을 자동으로 함께 설치합니다.

### 개발 환경 설치

프로젝트를 클론한 후, `mpcs/kipris_trademark_mcp` 디렉토리에서 다음 명령을 실행하여 편집 가능한 모드로 설치할 수 있습니다. (개발 및 테스트용)

```bash
# 가상 환경 생성 및 활성화 (Python 3.12 이상 권장)
uv venv .venv
source .venv/bin/activate

# 의존성 설치 (개발 의존성 포함)
uv pip install -e ".[dev]" 
```

## 3. 설정 및 AI 에이전트 연동

### 3.1. KIPRIS API 키 설정 (필수)

서버를 실행하거나 AI 에이전트에서 사용하기 전에 KIPRIS Open API 키를 **`KIPRIS_API_KEY`** 라는 이름의 환경 변수로 설정해야 합니다.
서버 내부의 `mcp_server/auth.py`에 정의된 `api_key_provider` 함수가 이 환경 변수를 읽어 `kipris-api-wrapper` 라이브러리에 전달합니다.

```bash
# 예시: KIPRIS_API_KEY 환경 변수 설정
export KIPRIS_API_KEY="YOUR_KIPRIS_API_KEY_HERE"
```

Cloud Run과 같은 배포 환경에서는 서비스 환경 변수로 `KIPRIS_API_KEY`를 설정하거나, Secret Manager에 저장된 값을 참조하여 주입하는 것을 권장합니다.

### 3.2. AI 에이전트 연동 (MCP 클라이언트 설정)

AI 에이전트(예: Cursor, Roo)에서 이 MCP 서버를 사용하려면 클라이언트의 MCP 설정 파일에 서버 정보를 등록해야 합니다. PyPI에 배포된 패키지를 `uvx`로 실행하는 경우, 다음과 같이 설정합니다.

```json
// 예시: AI 에이전트 MCP 설정 파일
{
  "mcpServers": {
    "kipris_trademark_mcp": { // 또는 원하는 서버 이름
      "command": "uvx",
      "args": [
        "--from", "kipris-trademark-mcp==0.1.0", // PyPI 패키지명 및 버전
        "kipris-mcp-server"                     // pyproject.toml의 [project.scripts]에 정의된 이름
      ],
      "env": { 
        "KIPRIS_API_KEY": "YOUR_KIPRIS_API_KEY_HERE" // 실제 KIPRIS API 키로 대체
      },
      "alwaysAllow": [ // 필요에 따라 도구별 alwaysAllow 설정
          "search_by_trademark_name",
          "search_by_application_number",
          "find_codes_by_product_name",
          "search_by_registration_number"
      ]
      // "disabled": false // 필요시 활성화/비활성화
    }
  }
}
```
**필수 환경 변수:**
*   `KIPRIS_API_KEY`: AI 에이전트 MCP 설정의 `env` 블록 또는 `uvx` 실행 환경에 이 환경 변수가 올바르게 설정되어 있어야 KIPRIS API를 사용하는 도구들이 정상 작동합니다.

### 3.3. 통합 테스트 설정 (개발자용)

통합 테스트(`tests/integration`) 실행 시에는 `mpcs/kipris_trademark_mcp/tests/integration/.env` 파일에 **`KIPRIS_TEST_API_KEY`** 라는 이름으로 테스트용 API 키를 설정해야 합니다.

```dotenv
# mpcs/kipris_trademark_mcp/tests/integration/.env (통합 테스트용)
KIPRIS_TEST_API_KEY="YOUR_KIPRIS_API_KEY_FOR_TESTING"
```
`tests/integration/conftest.py`의 `integration_api_key_provider` fixture가 이 파일을 로드하여 테스트에 사용합니다. **이 `.env` 파일은 Git 버전 관리에서 제외해야 합니다.**

## 4. 직접 실행 (uvx 사용)

터미널에서 `uvx`를 사용하여 MCP 서버를 직접 실행하고 테스트할 수 있습니다.

```bash
# KIPRIS_API_KEY 환경 변수 설정
export KIPRIS_API_KEY="YOUR_KIPRIS_API_KEY_HERE"

# uvx로 PyPI에서 패키지를 가져와 실행
uvx --from kipris-trademark-mcp==0.1.0 kipris-mcp-server
```
서버는 Stdio 모드로 실행됩니다.

로컬 개발 환경에서 소스 코드를 직접 실행하려면 다음을 참고하십시오:
```bash
# 가상 환경 활성화
source .venv/bin/activate

# KIPRIS_API_KEY 환경 변수 설정 (필요시)
# export KIPRIS_API_KEY="YOUR_KIPRIS_API_KEY_HERE"

# uv를 사용하여 등록된 스크립트 실행 (편집 가능한 모드로 설치된 경우)
uv run kipris-mcp-server
```

## 5. 제공 도구

이 서버는 다음과 같은 도구를 제공합니다.

### 5.1. `search_by_trademark_name`

*   **설명:** 상표명 및 선택적 필터(분류 코드, 유사군 코드, 출원인명 등)를 사용하여 KIPRIS에서 상표 정보를 검색합니다.
*   **입력 (`arguments`):**
    *   `trademark_name` (str, 필수): 검색할 상표명.
    *   `classification_codes` (list[str], 선택): NICE 분류 코드 리스트.
    *   `similarity_codes` (list[str], 선택): 유사군 코드 리스트.
    *   `applicant_name` (str, 선택): 출원인명.
    *   `rows` (int, 선택, 기본값 100): 페이지당 결과 수.
    *   `page_no` (int, 선택, 기본값 1): 페이지 번호.
*   **출력:**
    *   `total_count` (int): 총 검색 결과 수.
    *   `trademarks` (list[dict]): 검색된 상표 목록.

### 5.2. `search_by_application_number`

*   **설명:** 출원번호를 사용하여 특정 상표의 상세 정보를 검색합니다.
*   **입력 (`arguments`):**
    *   `application_number` (str, 필수): 검색할 출원번호.
*   **출력:**
    *   `trademark` (dict | None): 검색된 상표 정보 또는 `None`.

### 5.3. `find_codes_by_product_name`

*   **설명:** 상품 또는 서비스 명칭 키워드를 사용하여 관련된 NICE 분류 코드 및 유사군 코드 정보를 검색합니다.
*   **입력 (`arguments`):**
    *   `product_keyword` (str, 필수): 검색할 상품/서비스 키워드.
    *   `rows` (int, 선택, 기본값 100): 페이지당 결과 수.
    *   `page_no` (int, 선택, 기본값 1): 페이지 번호.
*   **출력:**
    *   `total_count` (int): 총 검색 결과 수.
    *   `product_codes` (list[dict]): 검색된 상품 코드 정보 목록.

### 5.4. `search_by_registration_number`
*   **설명:** 등록번호를 사용하여 특정 상표의 상세 정보를 검색합니다.
*   **입력 (`arguments`):**
    *   `registration_number` (str, 필수): 검색할 등록번호.
*   **출력:**
    *   `trademark` (dict | None): 검색된 상표 정보 또는 `None`.


## 6. 사용 예시 (Python `fastmcp` 클라이언트)

다음은 `fastmcp` 클라이언트를 사용하여 각 도구를 호출하는 예시입니다.

```python
import asyncio
from fastmcp import Client, MCPError

async def run_mcp_client():
    # Stdio를 통해 실행 중인 서버에 연결
    # 실제 사용 시에는 서버 실행 명령어와 프로세스 관리 필요
    # KIPRIS_API_KEY 환경 변수가 설정되어 있어야 함
    server_process_cmd = ["uvx", "--from", "kipris-trademark-mcp==0.1.0", "kipris-mcp-server"]

    try:
        async with Client.stdio(server_process_cmd) as client:
            print(f"Connected to server: {client.server_name}")

            # 예시 1: 상표명으로 검색
            try:
                print("\n--- Searching by trademark name 'ExampleBrand' ---")
                result_name = await client.use_tool(
                    "search_by_trademark_name",
                    {"trademark_name": "ExampleBrand", "rows": 5}
                )
                print(f"Found {result_name.get('total_count', 0)} trademarks.")
                for tm in result_name.get('trademarks', [])[:2]: # 처음 2개만 출력
                    print(f"  - App No: {tm.get('application_number')}, Name: {tm.get('trademark_name')}")
            except MCPError as e:
                print(f"Error using search_by_trademark_name: {e}")

            # (다른 도구 호출 예시 생략 - 필요시 추가)

    except Exception as e:
        print(f"Failed to connect or communicate with MCP server: {e}")

if __name__ == "__main__":
    # 실제 실행 전 KIPRIS_API_KEY 환경 변수 설정 필요
    import os
    if not os.environ.get("KIPRIS_API_KEY"):
        print("Error: KIPRIS_API_KEY environment variable is not set.")
        print("Please set it before running the example: export KIPRIS_API_KEY='your_key'")
    else:
        asyncio.run(run_mcp_client())
```

## 7. 상세 명세, 개발 계획 및 배포

*   [서버 상세 명세](./docs/spec.md)
*   [개발 태스크 목록](./docs/tasks.md)
*   [배포 및 사용 가이드](./docs/deployment_guide.md) (PyPI 배포 내용으로 업데이트 예정)

## 8. 기여

(기여 방법에 대한 안내 추가 예정)

## 9. 라이선스

MIT License ([LICENSE](LICENSE) 파일 참조)
