
chat_dict = dict()

def insert_msg(chatroom_id:int, user_type:str, msg: str):
    if chatroom_id in chat_dict:
        chat_dict[chatroom_id].append((user_type, msg))
    else:
        chat_list = list()
        chat_list.append((user_type, msg))
        chat_dict[chatroom_id] = chat_list

def get_chatroom_msg(chatroom_id:int) -> list:
    if chatroom_id not in chat_dict:
        return []
    return chat_dict[chatroom_id]
