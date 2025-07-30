# 생성 2025/04/29 17:04 아키텍트
# 수정 2025/04/29 22:03 아키텍트

import asyncio
import logging
from typing import Optional, Dict, Any

from kipris_api_wrapper import KiprisClient
from kipris_api_wrapper.exceptions import (
    KiprisApiClientError,
    KiprisApiError,
    MissingAPIKeyError,
)
from kipris_api_wrapper.models import TrademarkSearchResponse
from mcp_server.auth import api_key_provider # 임포트 추가

logger = logging.getLogger(__name__)

async def run(application_number: str) -> Optional[Dict[str, Any]]: # client 인자 제거
    """
    출원번호를 사용하여 KIPRIS에서 상표 정보를 검색합니다.

    Args:
        application_number: 검색할 상표의 출원번호 (필수, 형식: "40-YYYY-NNNNNNN")

    Returns:
        검색된 첫 번째 상표 정보 (JSON 호환 딕셔너리) 또는 결과가 없거나 오류 발생 시 오류 메시지 딕셔너리.
    """
    try:
        client = await KiprisClient.get_instance(api_key_provider=api_key_provider) # KiprisClient 인스턴스 생성
        # kipris-api-wrapper의 application_number 파라미터를 사용하여 검색합니다.
        response: TrademarkSearchResponse = await client.search_advanced_trademark(
            application_number=application_number, # application_number 인자 사용
            rows=1 # 첫 번째 결과만 필요하므로 rows=1 설정
        )

        if response and response.items:
            # 첫 번째 결과만 반환
            return response.items[0].model_dump(mode='json')
        else:
            logger.info(f"출원번호 '{application_number}'에 대한 상표 정보를 찾을 수 없습니다.")
            # 결과가 없을 경우 오류가 아니므로 None 반환 유지
            return None

    except MissingAPIKeyError:
        error_msg = "KIPRIS API 키가 설정되지 않았습니다."
        logger.error(error_msg)
        return {"error": error_msg} # 수정: 오류 메시지 딕셔너리 반환
    except KiprisApiClientError as e:
        error_msg = f"KIPRIS API 클라이언트 오류: {e}"
        logger.error(f"KIPRIS API 클라이언트 오류 발생 (출원번호: {application_number}): {e}")
        return {"error": error_msg} # 수정: 오류 메시지 딕셔너리 반환
    except KiprisApiError as e:
        error_msg = f"KIPRIS API 오류: {e}"
        logger.error(f"KIPRIS API 오류 발생 (출원번호: {application_number}): {e}")
        return {"error": error_msg} # 수정: 오류 메시지 딕셔너리 반환
    except Exception as e:
        error_msg = f"예상치 못한 오류 발생: {e}"
        logger.exception(f"search_by_application_number 도구 실행 중 예상치 못한 오류 발생 (출원번호: {application_number}): {e}")
        return {"error": error_msg} # 수정: 오류 메시지 딕셔너리 반환