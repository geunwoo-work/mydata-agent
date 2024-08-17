import os
import importlib

# 현재 디렉토리에서 모든 Python 파일을 찾고 모듈을 import
current_dir = os.path.dirname(__file__)
VECTOR_STORES = dict()

# 디렉토리 내의 모든 .py 파일을 가져옵니다
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename != "__init__.py" and filename != "abstract_store.py":
        module_name = filename[:-3]
        module = importlib.import_module(f".{module_name}", package="vector_store")
        
        # 모듈 내의 모든 클래스 인스턴스를 생성합니다
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and attr.__module__ == module.__name__: # 해당 파일에서 import하지 않고 직접 선언한 클래스인 경우
                instance = attr()
                VECTOR_STORES[attr_name] = instance
