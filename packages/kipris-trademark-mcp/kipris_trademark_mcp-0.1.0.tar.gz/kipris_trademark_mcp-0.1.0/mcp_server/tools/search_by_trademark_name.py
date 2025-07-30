# 생성 2025/04/29 17:01 아키텍트
# 수정 2025/05/01 12:18 Debug

import asyncio
import logging
from typing import List, Optional, Dict, Any, Union

from kipris_api_wrapper import KiprisClient
from kipris_api_wrapper.exceptions import (
    KiprisApiClientError,
    KiprisApiError,
    MissingAPIKeyError,
)
from kipris_api_wrapper.models import TrademarkSearchResponse

from mcp_server.auth import api_key_provider

logger = logging.getLogger(__name__)

async def run(
    trademark_name: str,
    classification_codes: Union[List[str], None] = None,
    similarity_codes: Union[List[str], None] = None,
    applicant_name: Union[str, None] = None,
    rows: int = 100,
    page_no: int = 1,
) -> Dict[str, Any]:
    """
    상표명 및 선택적 필터를 사용하여 KIPRIS에서 상표 정보를 검색합니다.

    Args:
        trademark_name: 검색할 상표 명칭 (필수)
        classification_codes: NICE 분류 코드 리스트 (선택 사항)
        similarity_codes: 유사군 코드 리스트 (선택 사항)
        applicant_name: 출원인 명칭 (선택 사항)
        rows: 페이지당 결과 수 (기본값 100)
        page_no: 페이지 번호 (기본값 1)

    Returns:
        검색 결과 (JSON 호환 딕셔너리) 또는 오류 발생 시 빈 딕셔너리.
    """
    try:
        client = await KiprisClient.get_instance(api_key_provider=api_key_provider)
        response: TrademarkSearchResponse = await client.search_advanced_trademark(
            trademark_name=trademark_name,
            classification_codes=classification_codes,
            similarity_codes=similarity_codes,
            applicant_name=applicant_name,
            rows=rows,
            page_no=page_no,
        )
        return response.model_dump(mode='json')

    except MissingAPIKeyError:
        logger.error("KIPRIS API 키가 설정되지 않았습니다.")
        # TODO: MCP 서버 레벨의 표준 오류 응답 구조 정의 필요
        return {"error": "API key is missing."}
    except KiprisApiClientError as e:
        logger.error(f"KIPRIS API 클라이언트 오류 발생: {e}")
        return {"error": f"KIPRIS client error: {e}"}
    except KiprisApiError as e:
        logger.error(f"KIPRIS API 오류 발생: {e}")
        return {"error": f"KIPRIS API error: {e}"}
    except Exception as e:
        logger.exception(f"search_by_trademark_name 도구 실행 중 예상치 못한 오류 발생: {e}")
        return {"error": f"An unexpected error occurred: {e}"}