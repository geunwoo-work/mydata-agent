import logging
from logging.handlers import RotatingFileHandler

# 공통 로깅 포맷
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')

# 파일 핸들러 생성 함수
def create_file_handler(filename, level=logging.INFO, max_bytes=5000000, backup_count=5):
    handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler

# 로거 생성 및 설정 함수
def get_logger(name, level=logging.INFO, handlers=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if handlers:
        for handler in handlers:
            logger.addHandler(handler)
    return logger

# 로깅 설정
def setup_loggers():
    # 개별 로거 설정
    logger_fastapi = get_logger('fastapi', handlers=[create_file_handler('log/fastapi.log')])
    logger_vector_store = get_logger('vector_store', handlers=[create_file_handler('log/vector_store.log')])
    logger_llm = get_logger('llm', handlers=[create_file_handler('log/llm.log')])

    # 로거 등록
    return {
        'fastapi': logger_fastapi,
        'vector_store': logger_vector_store,
        'logger_llm': logger_llm,
    }

loggers = setup_loggers()
