# 생성 2025/04/29 16:55 아키텍트
# 수정 2025/05/05 15:47 Code (main 함수 분리)
# 수정 2025/05/01 17:19 Debug

import sys
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler # 핸들러 추가
from fastmcp import FastMCP
from .tools import search_by_trademark_name, search_by_application_number, find_codes_by_product_name, search_by_registration_number

# --- 로깅 설정 수정 ---
# TODO: 로그 파일 위치를 사용자 홈, 임시 디렉토리 또는 환경 변수로 변경 고려
log_file_path = Path(__file__).parent / "mcp_server.log" # 로그 파일 경로
log_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(pathname)s:%(lineno)d] - %(message)s'
)

# 파일 핸들러 설정 (예: RotatingFileHandler 사용)
file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=3, encoding='utf-8') # 10MB, 3개 백업
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

# 루트 로거 설정
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
# 기존 핸들러 제거 (basicConfig에 의해 추가된 핸들러가 있을 수 있음)
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)
root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__) # 현재 모듈 로거 가져오기
# ---------------------

# FastMCP 인스턴스 생성
mcp = FastMCP("kipris-trademark-mcp")

# 도구 등록
mcp.tool(name="search_by_trademark_name")(search_by_trademark_name.run)
mcp.tool(name="search_by_application_number")(search_by_application_number.run)
mcp.tool(name="find_codes_by_product_name")(find_codes_by_product_name.run)
mcp.tool(name="search_by_registration_number")(search_by_registration_number.run)

def main():
    """MCP 서버를 시작하는 메인 함수"""
    try:
        logger.info("Attempting to start MCP server...")
        mcp.run(transport='stdio')
    except Exception as e:
        logger.exception(f"Failed to run MCP server: {e}") # 파일에도 traceback 로깅됨
        sys.exit(1)

if __name__ == "__main__":
    main()
