# 생성 2025/04/29 21:24 아키텍트
# 수정 2025/05/10 17:15 Code

import asyncio
import logging
from typing import Any, Dict, Optional

from kipris_api_wrapper import (
    KiprisClient,
    KiprisApiError,
    KiprisApiClientError,
    MissingAPIKeyError,
)
from mcp_server.auth import api_key_provider

logger = logging.getLogger(__name__)


async def run(registration_number: str) -> Optional[Dict[str, Any]]:
    """
    등록번호를 사용하여 KIPRIS에서 상표 정보를 검색합니다.

    Args:
        registration_number: 검색할 상표의 등록번호 (필수, 형식: "40-NNNNNNN")

    Returns:
        검색된 첫 번째 상표 정보 (JSON 호환 딕셔너리) 또는 결과가 없거나 오류 발생 시 오류 메시지를 포함한 딕셔너리.
    """
    if not registration_number:
        logger.error("등록번호가 제공되지 않았습니다.")
        return {"error": "등록번호가 제공되지 않았습니다."}

    try:
        # KiprisClient 인스턴스를 가져옵니다. API 키 제공자를 전달합니다.
        client = await KiprisClient.get_instance(api_key_provider=api_key_provider)

        # search_advanced_trademark 메서드를 호출하여 상표 정보를 검색합니다.
        # 등록번호를 인자로 전달하고, 첫 번째 결과만 필요하므로 rows=1로 설정합니다.
        # 해당 메서드는 비동기 함수이므로 await를 사용하여 호출합니다.
        response = await client.search_advanced_trademark(
            registration_number=registration_number,
            rows=1,
        )

        # 응답이 있고, 응답 내에 items 리스트가 비어있지 않은 경우
        if response and response.items:
            # 첫 번째 검색 결과를 JSON 호환 딕셔너리로 변환하여 반환합니다.
            return response.items[0].model_dump(mode="json")
        else:
            # 검색 결과가 없는 경우 정보 로그를 남기고 오류 메시지를 포함한 딕셔너리를 반환합니다.
            logger.info(f"등록번호 '{registration_number}'에 대한 검색 결과가 없습니다.")
            return {"error": f"등록번호 '{registration_number}'에 대한 검색 결과가 없습니다."}

    except MissingAPIKeyError:
        # API 키가 누락된 경우 오류 로그를 남기고 오류 메시지를 포함한 딕셔너리를 반환합니다.
        logger.error(f"KIPRIS API 키가 설정되지 않았습니다. (등록번호: {registration_number})")
        return {"error": "KIPRIS API 키가 설정되지 않았습니다."}
    except KiprisApiError as e:
        # KIPRIS API 자체 오류 발생 시 오류 로그를 남기고 오류 메시지를 포함한 딕셔너리를 반환합니다.
        logger.error(f"KIPRIS API 오류 발생 (등록번호: {registration_number}): {e}")
        return {"error": f"KIPRIS API 오류: {e}"}
    except KiprisApiClientError as e:
        # KIPRIS API 클라이언트 관련 오류 발생 시 오류 로그를 남기고 오류 메시지를 포함한 딕셔너리를 반환합니다.
        logger.error(f"KIPRIS API 클라이언트 오류 발생 (등록번호: {registration_number}): {e}")
        return {"error": f"KIPRIS API 클라이언트 오류: {e}"}
    except Exception as e:
        # 그 외 예상치 못한 오류 발생 시 예외 로그를 남기고 오류 메시지를 포함한 딕셔너리를 반환합니다.
        logger.exception(f"등록번호로 상표 검색 중 예상치 못한 오류 발생 (등록번호: {registration_number}): {e}")
        return {"error": f"예상치 못한 오류 발생: {e}"}