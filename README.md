# mydata-agent
마이데이터 공식 문서를 기반으로 정책과 기술 사양 등을 답변해주는 에이전트 입니다.  
해당 프로젝트는 파이썬 **3.12.5 버전**에서 개발되었습니다.

## 프로젝트 실행 및 사용
#### poetry 설치
기존에 poetry를 사용중이라면 건너뛰셔도 좋습니다.  
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
#### package 설치
운영 환경:
```sh
poetry install --without dev
```
개발 환경(test 환경 포함):
```sh
poetry install
```
#### 등록 혹은 변경되어야 하는 변수
```sh
# 현재 프로젝트의 운영 환경을 설정합니다
.env
settings="prod" # pytest를 진행하거나 개발중일 때는 prod 대신 dev로 설정

# OPENAI KEY값 설정
app/settings/base/KEY_CONF.py
...
OPENAI_API_KEY="your api key"
...
```
#### 테스트 코드 실행
테스트 환경에서는 Vector store를 삭제 후 재생성 하는 로직이 존재하기 때문에 전체 파일에 대해 매번 embedding을 실행하면 비효율적입니다.  
그런 이유로 `app/data/test` 디렉토리 하위에 있는 작은 pdf 파일을 활용하여 테스트 할때마다 embedding을 하여 vector store를 구성하도록 하였습니다.
```sh
./run_test.sh
```
#### 프로젝트 실행
```sh
./run_uvicorn.sh # prod 환경에서 최초 실행 시 vector store 생성을 위해 시간이 다소 소요될 수 있습니다.
```
#### 웹 접속 방법 및 사용 방법
- `http://localhost:8000/docs` 로 접속하여 api 테스트 진행
- 실행하고 싶은 api 선택 후 우측의 `Try it out` 버튼 클릭
- parameter과 body 값을 채운 후 하단의 `Execute` 버튼 클릭
- 하단의 Response 확인

## api 설명
멀티턴 에이전트 로직 구현을 위해 Chatroom이라는 개념을 만들었습니다.  
과거 대화 내역 기록은 동일 chatroom 내에서만 이루어지며 대화 내역은 db에 저장됩니다.  
현재 해당 프로젝트에서는 연결된 db가 없기 때문에 mock_db에 간단히 구현하였습니다.  
멀티턴 에이전트 로직을 사용하고 싶다면 동일한 `chatroom_id` 값을 path_parameter로 넣으시면 됩니다.  
단, 메모리상에 올라가는 간단한 mock_db를 활용하였기 때문에 프로그램 종료 후 재시작 시, 기존 대화내역들은 모두 사라집니다.  
각 api의 input/output 예시는 `http://localhost:8000/docs` 에서 확인 가능합니다.
#### Get Chatroom Message
`{chatroom_id}` 방에 존재하는 모든 대화 내역들을 가져옵니다.
```sh
GET /v1/chatrooms/{chatroom_id}/messages

path_parameter
(Required) chatroom_id (int) : 과거 대화 내역을 가져오기 위한 chatroom_id입니다. 현재는 아무 숫자 값이나 넣으면 됩니다.
```
#### Create Chatroom Message
`{chatroom_id}` 방에 새로운 질문을 생성합니다.
```sh
POST /v1/chatrooms/{chatroom_id}/messages

path_parameter
(Required) chatroom_id (int) : 과거 대화 내역을 가져오기 위한 chatroom_id입니다. 현재는 아무 숫자 값이나 넣으면 됩니다.

body
(Required) message (str) : 에이전트에게 물어볼 질문 내용이 담긴 메세지 입니다.
(Required) llm_type (str) : 에이전트가 사용하는 llm의 종류입니다. 현재는 OpenaiChain만 사용 가능합니다.
(Required) llm_model_name (str) : 해당 llm에서 사용하고 싶은 모델이름 정보입니다. 현재 Openai에서 제공하는 LLM 모델 명을 넣으면 됩니다.
```

## 프로젝트 설명 및 구조
해당 프로젝트는 마이데이터 공식 문서를 가져와 해당 문서를 embedding하여 vector store에 저장하는 것에서 시작됩니다.  
이미 저장이 되어 있다면 저장된 vector store를 load하여 메모리에 가지고 있다가 쿼리 요청이 들어오면 store에서 해당 쿼리와 가장 비슷한 context를 추출합니다.  
이후 해당 쿼리와 chatroom에 존재하는 chat_history, context를 포함하여 LLM에게 답변 생성 요청을 보내게 되고 이를 api 요청의 리턴값으로 돌려줍니다.
```bash
├── app
│   ├── chain           # langchain의 chain을 관리하기 위한 디렉토리입니다. 현재는 OpenaiChain만 존재하지만 추후 추가 가능하며 종류를 선택할 수 있습니다.
│   ├── conf            # 프로젝트 설정과 관련된 파일을 관리하기 위한 디렉토리입니다. 현재는 로거 설정 파일이 존재합니다.
│   ├── data            # 마이데이터 공식 문서 데이터 및 vector store을 저장 및 load하는 역할을 하는 디렉토리 입니다.
│   ├── log             # 로그 파일 관리를 위한 디렉토리입니다.
│   ├── mock_db         # 임시로 구현한 mock db 관련 로직이 존재하는 디렉토리입니다. db 도입시 변경되어야 합니다.
│   ├── prompt          # prompt 관리를 위한 디렉토리 입니다. LLM 종류마다 사용되는 프롬프트의 형식과 한글, 영어 프롬프트 등 프롬프트를 활용한 다양한 실험을 위해 존재하는 디렉토리입니다.
│   ├── routers         # FastAPI router 관리용 디렉토리 입니다.
│   │   └── v1          # api를 버전별로 관리하기 위해 별도의 디렉토리를 생성하였습니다.
│   ├── settings        # 개발환경과 운영환경에서 다르게 사용되는 변수 관리를 위한 디렉토리 입니다.
│   │   ├── base        # 개발환경과 운영환경에서 공통으로 사용되는 변수를 관리하는 디렉토리 입니다.
│   │   ├── dev         # 개발환경에서 사용되는 변수 관리용 디렉토리입니다.
│   │   └── prod        # 운영환경에서 사용되는 변수 관리용 디렉토리입니다.
│   ├── tests           # pytest용 디렉토리입니다.
│   ├── utils           # custom exception, enum과 같이 다양한 디렉토리에서 공용으로 사용되는 파일을 위한 디렉토리입니다.
│   └── vector_store    # vector store 관리용 디렉토리 입니다.
├── main.py             # ./run_uvicorn을 하면 해당 파일이 실행됩니다.
├── .env                # 개발환경인지 운영환경인지 구분해주는 변수를 선언합니다.
├── run_test.sh         # 간편한 테스팅을 위한 쉘스크립트 입니다.
└── run_uvicorn.sh      # 간편한 실행을 위한 쉘스크립트 입니다.
``` 