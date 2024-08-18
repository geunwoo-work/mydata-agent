from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_chatroom_message_with_correct_input():
    request_payload = {
        "message": "거점중계기관이 뭐야?",
        "llm_type": "OpenaiChain",
        "llm_model_name": "gpt-4o"
    }

    response = client.post("/v1/chatrooms/1/messages", json=request_payload)
    
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["chatroom_id"] == 1
    assert len(response_json["answer_message"]) > 0

def test_create_chatroom_message_with_wrong_llm_type():
    request_payload = {
        "message": "거점중계기관이 뭐야?",
        "llm_type": "OpenAiChain",
        "llm_model_name": "gpt-4o"
    }

    response = client.post("/v1/chatrooms/1/messages", json=request_payload)
    
    assert response.status_code == 400

def test_create_chatroom_message_with_wrong_llm_model_name():
    request_payload = {
        "message": "거점중계기관이 뭐야?",
        "llm_type": "OpenaiChain",
        "llm_model_name": "gpt-3.5-turbo-125"
    }

    response = client.post("/v1/chatrooms/1/messages", json=request_payload)
    
    assert response.status_code == 400

def test_get_chatroom_message():
    response = client.get("/v1/chatrooms/1/messages")

    assert response.status_code == 200
