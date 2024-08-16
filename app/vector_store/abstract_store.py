import asyncio
import os
from abc import ABC, abstractmethod
from langchain_community.document_loaders import PyPDFLoader
from conf.log_conf import loggers

log = loggers['vector_store']

class VectorStore(ABC):
    def __init__(self):
        self._vector_store = None
        self._building_store = False
        self._path = None
    
    @abstractmethod
    async def _create_vector_store(self):
        pass

    @abstractmethod
    def _load_vector_store(self):
        pass
    
    @abstractmethod
    def get_vector_store(self):
        pass

    @classmethod
    def _get_files_from_directory(cls, directory_path: str, extension: str = None) -> list:
        file_list = list()
        for f in os.listdir(directory_path):
            if extension and not f.endswith('.' + extension):
                continue
            file_list.append(os.path.join(directory_path, f))
        return file_list

    async def _load_files(self, file_path: str, extension: str):
        if extension == 'pdf':
            loader = PyPDFLoader(file_path)
        else: # TODO: add other loaders
            log.info(f"{extension} extension does not support!")
            return []
        documents = await loader.aload()
        return documents

    async def _load_files_from_directory(self, directory_path: str, extension: str) -> list:
        files = self._get_files_from_directory(directory_path, extension)
        if len(files) == 0:
            log.error(f"No any {extension} files under this directory: {directory_path}")
            raise FileNotFoundError(f"No any {extension} files under this directory: {directory_path}")
        
        tasks = [self._load_files(file_path, extension) for file_path in files]
        task_results = await asyncio.gather(*tasks)

        combined_documents = list()
        for documents in task_results:
            combined_documents.extend(documents)
        return combined_documents
