from abc import ABC, abstractmethod
import os

class VectorStore(ABC):
    _vector_store = None
    _building_store = False

    def __init__(self):
        pass
    
    @abstractmethod
    async def _load_vector_store(self):
        pass
    
    @abstractmethod
    async def retrieve(self):
        pass

    @classmethod
    def _get_files_from_directory(self, directory_path: str, extension: str = None) -> list:
        file_list = list()
        for f in os.listdir(directory_path):
            if extension and not f.endswith('.' + extension):
                continue
            file_list.append(os.path.join(directory_path, f))
        return file_list
