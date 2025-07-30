# 생성 2025/04/29 17:00 아키텍트
# 수정 2025/05/06 15:00 Code (환경 변수 사용 방식으로 변경)

import logging
import os
# kipris_api_wrapper에서 정의한 예외 사용
from kipris_api_wrapper.exceptions import MissingAPIKeyError

logger = logging.getLogger(__name__)

async def api_key_provider() -> str:
    """
    실행 환경의 환경 변수에서 KIPRIS API 키를 로드하여 반환합니다.
    환경 변수 이름: KIPRIS_API_KEY
    """
    api_key = os.environ.get("KIPRIS_API_KEY")

    if not api_key:
        error_msg = "KIPRIS_API_KEY 환경 변수가 설정되지 않았습니다."
        logger.error(error_msg)
        # kipris_api_wrapper와 일관성을 위해 MissingAPIKeyError 사용
        raise MissingAPIKeyError(error_msg)

    logger.debug("KIPRIS API Key loaded from environment variable.")
    return api_key