import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from vector_store.abstract_store import VectorStore
from conf.log_conf import loggers

log = loggers['vector_store']

class FaissStore(VectorStore):
    def __init__(self):
        super().__init__()

    async def _create_vector_store(self, directory_path: str, extension: str, embedding_model: str,
                                    chunk_size: int, chunk_overlap: int):
        combined_documents = await self._load_files_from_directory(directory_path, extension)
        text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        docs = text_spliter.split_documents(combined_documents)
        
        embeddings = OpenAIEmbeddings(model=embedding_model)
        db = await FAISS.afrom_documents(docs, embeddings)
        db.save_local(self._path)
        return db
    
    def _load_vector_store(self, embedding_model):
        embeddings = OpenAIEmbeddings(model=embedding_model)
        db = FAISS.load_local(self._path, embeddings)
        return db
    
    async def initialize(self, directory_path: str, extension: str, embedding_model: str,
                        chunk_size: int, chunk_overlap: int):
        if self._vector_store is not None:
            return
        self._building_store = True
        self._path = f"{directory_path}/faiss/{extension}_{embedding_model}_{chunk_size}_{chunk_overlap}"
        if os.path.exists(self._path): # 파일이 존재하면
            self._vector_store = await self._load_vector_store()
        else:
            log.info("Start create vector store")
            db = await self._create_vector_store(directory_path, extension, embedding_model,
                                                chunk_size, chunk_overlap)
            self._vector_store = db
            log.info("End create vector store")
        self._building_store = False

    async def renew_vector_store(self, directory_path: str, extension: str, embedding_model: str,
                        chunk_size: int, chunk_overlap: int):
        self._building_store = True
        self._path = f"{directory_path}/faiss/{extension}_{embedding_model}_{chunk_size}_{chunk_overlap}"
        db = await self._create_vector_store(directory_path, extension, embedding_model,
                                            chunk_size, chunk_overlap)
        self._vector_store = db
        self._building_store = False

    def get_vector_store(self):
        return self._vector_store
