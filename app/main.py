from fastapi import FastAPI
from routers.chatrooms import chatrooms

app = FastAPI()
app.include_router(chatrooms)
