from fastapi import APIRouter
from pydantic import BaseModel, Field
from conf.log_conf import loggers

chatrooms = APIRouter(prefix='/chatrooms')

logger = loggers['fastapi']

class ChatroomMessage(BaseModel):
    message: str = Field(example="토큰이 중복 발급되었을 경우 어떻게 되나요?")

@chatrooms.post('/{chatroom_id}', tags=['chatrooms'])
async def chatroom_message(chatroom_id: int, message: ChatroomMessage):
    return {"msg": "success"}
