from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.chatrooms import chatrooms
from vector_store.faiss import FaissStore
from chain.open_ai import OpenAiChain
from utils.key_conf import KEY_CONF
from prompt.en import MARKDOWN_SYSTEM_PROMPT, MARKDOWN_CONTEXT_PROMPT
import os

async def start():
    data_path = KEY_CONF.DATA_PATH
    extension = KEY_CONF.EXTENSION
    embedding_model = KEY_CONF.EMBEDDING_MODEL
    chunk_size = KEY_CONF.CHUNK_SIZE
    chunk_overlap = KEY_CONF.CHUNK_OVERLAP
    faiss = FaissStore()
    await faiss.initialize(data_path, extension, embedding_model, chunk_size, chunk_overlap)
    # open_ai_model = KEY_CONF.OPENAI_MODEL
    # chain = OpenAiChain(open_ai_model)
    # system_message = MARKDOWN_SYSTEM_PROMPT
    # context_prompt = MARKDOWN_CONTEXT_PROMPT
    # chat_history = [("user", "거점중계기관이 뭐야?"), ("assistant", "거점중계기관은 금융보안원이나 다른 정보제공자를 대신하여 고객의 요청에 따라 개인신용정보를 다른 정보수신자에게 전송하는 기관을 말합니다.")]
    # query = "방금 대답 영어로 해줘"
    # context_list = await faiss.retrieve(query)
    # formatted_context = [f"{i+1}. {item}" for i, item in enumerate(context_list)]
    # context = context_prompt + "  ".join(formatted_context)
    # result = await chain.invoke(system_message, context, query, chat_history)

    
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
