from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.chatrooms import chatrooms
from vector_store.faiss import FaissStore
from utils.key_conf import KEY_CONF
import os

async def start():
    data_path = KEY_CONF.DATA_PATH
    extension = KEY_CONF.EXTENSION
    embedding_model = KEY_CONF.EMBEDDING_MODEL
    chunk_size = KEY_CONF.CHUNK_SIZE
    chunk_overlap = KEY_CONF.CHUNK_OVERLAP
    faiss = FaissStore()
    await faiss.initialize(data_path, extension, embedding_model, chunk_size, chunk_overlap)

    
def shutdown():
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.
    await start()
    
    yield
    
    # When service is stopped.
    shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(chatrooms)
