import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from vector_store.abstract_store import VectorStore, log
from utils.exception import BuildingStoreException, InitializationException

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
        db = FAISS.load_local(
            folder_path = self._path,
            embeddings = embeddings,
            allow_dangerous_deserialization = True
        )
        return db
    
    async def initialize(self, directory_path: str, extension: str, embedding_model: str,
                        chunk_size: int, chunk_overlap: int) -> None:
        if self._vector_store is not None:
            return
        self._building_store = True
        self._path = f"{directory_path}/faiss/{extension}_{embedding_model}_{chunk_size}_{chunk_overlap}"
        if os.path.exists(self._path): # 파일이 존재하면
            log.info("Load vector store")
            self._vector_store = self._load_vector_store(embedding_model)
        else:
            log.info("Start create vector store")
            db = await self._create_vector_store(directory_path, extension, embedding_model,
                                                chunk_size, chunk_overlap)
            self._vector_store = db
            log.info("End create vector store")
        self._building_store = False

    async def renew_vector_store(self, directory_path: str, extension: str, embedding_model: str,
                        chunk_size: int, chunk_overlap: int) -> None:
        self._building_store = True
        self._path = f"{directory_path}/faiss/{extension}_{embedding_model}_{chunk_size}_{chunk_overlap}"
        db = await self._create_vector_store(directory_path, extension, embedding_model,
                                            chunk_size, chunk_overlap)
        self._vector_store = db
        self._building_store = False

    def get_vector_store(self):
        return self._vector_store

    async def retrieve(self, query:str, k_num: int = 3) -> list:
        if self._building_store:
            raise BuildingStoreException("Building vector store work not completed!")
        elif self._vector_store is None:
            log.error("initialize function does not called!")
            raise InitializationException("Vector store initialization work does not started!")
        docs = await self._vector_store.asimilarity_search(query, k=k_num)
        result = [doc.page_content for doc in docs]
        return result
