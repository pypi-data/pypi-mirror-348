# 생성 2025/04/29 17:07 아키텍트
# 수정 2025/04/29 17:59 아키텍트

import asyncio
import logging
from typing import Dict, Any, Optional

from kipris_api_wrapper import KiprisClient  # KiprisApiClient -> KiprisClient
from kipris_api_wrapper.exceptions import (
    KiprisApiClientError,
    KiprisApiError,
    MissingAPIKeyError,
)
from kipris_api_wrapper.models import ProductCodeSearchResponse

from mcp_server.auth import api_key_provider # 주석 제거

logger = logging.getLogger(__name__)

async def run(
    # client: KiprisApiClient, # client 인자 제거
    product_keyword: str,
    rows: int = 100,
    page_no: int = 1,
) -> Optional[Dict[str, Any]]: # 반환 타입 Optional 추가
    """
    상품명 키워드를 사용하여 KIPRIS에서 상품 분류 및 유사군 코드를 검색합니다.

    Args:
        # client: KiprisApiClient 인스턴스 # client 설명 제거
        product_keyword: 검색할 상품명 키워드 (필수)
        rows: 페이지당 결과 수 (기본값 100)
        page_no: 페이지 번호 (기본값 1)

    Returns:
        검색 결과 (JSON 호환 딕셔너리) 또는 오류 발생 시 None.
    """
    try:
        client = await KiprisClient.get_instance(api_key_provider=api_key_provider) # client 인스턴스 내부 생성
        response: ProductCodeSearchResponse = await client.search_product_info(
            product_keyword=product_keyword,
            rows=rows,
            page_no=page_no,
        )
        return response.model_dump(mode='json')

    except MissingAPIKeyError:
        error_msg = "API key is missing." # 테스트 기대값과 정확히 일치
        logger.error("KIPRIS API 키가 설정되지 않았습니다.")
        return {"error": error_msg} # 오류 시 딕셔너리 반환
    except KiprisApiClientError as e:
        error_msg = f"KIPRIS client error: {e}" # 테스트 기대값과 정확히 일치
        logger.error(f"KIPRIS API 클라이언트 오류 발생: {e}")
        return {"error": error_msg} # 오류 시 딕셔너리 반환
    except KiprisApiError as e:
        error_msg = str(e) # KiprisApiError의 __str__ 메서드를 사용하여 오류 메시지 생성
        logger.error(f"KIPRIS API 오류 발생: {e}")
        return {"error": error_msg} # 오류 시 딕셔너리 반환
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}" # 테스트 코드와 메시지 형식 일치
        logger.exception(f"find_codes_by_product_name 도구 실행 중 예상치 못한 오류 발생: {e}")
        return {"error": error_msg} # 오류 시 딕셔너리 반환