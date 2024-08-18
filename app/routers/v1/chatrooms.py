import traceback
from fastapi import APIRouter, Path, Body, HTTPException
from pydantic import BaseModel
from conf.log_conf import loggers
from utils.enums import VectorStoreType
from vector_store import VECTOR_STORES
from chain import CHAIN_STORES
from mock_db.api import insert_msg, get_chatroom_msg
from prompt.en import MARKDOWN_SYSTEM_PROMPT, MARKDOWN_CONTEXT_PROMPT
from utils.exception import BuildingStoreException, InitializationException


chatrooms = APIRouter(prefix='/v1/chatrooms')

log = loggers['fastapi']
faiss = VECTOR_STORES[VectorStoreType.FAISS]

class ChatroomMessageList(BaseModel):
    chatroom_id: int
    messages: list

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "chatroom_id": 1,
                    "messages": [
                        [
                            "user",
                            "거점중계기관이 뭐야?"
                        ],
                        [
                            "assistant",
                            "거점중계기관은 정보제공자를 대신하여 고객의 요청에 따라 개인신용정보를 다른 정보수신자에게 전송하는 기관을 말합니다."
                        ],
                        [
                            "user",
                            "방금 대답 영어로 해줘"
                        ],
                        [
                            "assistant",
                            "A central relay agency is an organization that transmits personal credit information to other information recipients on behalf of information providers at the request of customers."
                        ]
                    ]
                }
            ]
        }
    }

@chatrooms.get('/{chatroom_id}/messages', tags=['chatrooms'])
def get_chatroom_message(chatroom_id: int = Path(...)) -> ChatroomMessageList:
    messages = get_chatroom_msg(chatroom_id)
    result = ChatroomMessageList(chatroom_id=chatroom_id, messages=messages)
    return result


class QueryMessage(BaseModel):
    message: str
    llm_type: str
    llm_model_name: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "거점중계기관이 뭐야?",
                    "llm_type": "OpenaiChain",
                    "llm_model_name": "gpt-3.5-turbo-0125",
                }
            ]
        }
    }

class QueryMessageResponse(BaseModel):
    chatroom_id: int
    answer_message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "chatroom_id": 1,
                    "answer_message": "거점중계기관은 정보제공자를 대신하여 고객의 요청에 따라 개인신용정보를 다른 정보수신자에게 전송하는 기관입니다.",
                }
            ]
        }
    }

@chatrooms.post('/{chatroom_id}/messages', tags=['chatrooms'], response_model=QueryMessageResponse)
async def create_chatroom_message(chatroom_id: int = Path(...),
                                query_message: QueryMessage = Body(...)) -> QueryMessageResponse:
    try:
        chain = CHAIN_STORES[query_message.llm_type]
        chain.set_model_name(query_message.llm_model_name)
        system_message = MARKDOWN_SYSTEM_PROMPT
        context = ""
        context_list = await faiss.retrieve(query_message.message)
    except BuildingStoreException as e:
        log.info(e)
        raise HTTPException(status_code=503, detail="Vector Store is not ready")
    except InitializationException as e:
        log.error(e)
        raise HTTPException(status_code=503, detail="Vector Store is not ready")
    except KeyError as e:
        log.info(e)
        raise HTTPException(status_code=400, detail="Check input value")
    except Exception as e:
        log.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if len(context_list) > 0:
        formatted_context = [f"{i+1}. {item}" for i, item in enumerate(context_list)]
        context = MARKDOWN_CONTEXT_PROMPT + "  ".join(formatted_context)
    chat_history = get_chatroom_msg(chatroom_id)

    try:
        chain_result = await chain.invoke(
            system_message,
            context,
            query_message.message,
            chat_history
        )
    except Exception as e:
        log.info(e)
        raise HTTPException(status_code=400, detail="Check input value")

    insert_msg(chatroom_id, "user", query_message.message)
    insert_msg(chatroom_id, "assistant", chain_result)
    result = QueryMessageResponse(chatroom_id=chatroom_id, answer_message=chain_result)
    return result

