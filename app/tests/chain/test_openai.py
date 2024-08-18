import pytest
from chain import CHAIN_STORES
from utils.key_conf import KEY_CONF
from utils.enums import LargeLanguageModelType
from prompt.en import MARKDOWN_QUERY_SYSTEM_PROMPT, MARKDOWN_CONTEXT_PROMPT

chain = CHAIN_STORES[LargeLanguageModelType.OPENAI]

@pytest.mark.asyncio
async def test_invoke():
    system_message = MARKDOWN_QUERY_SYSTEM_PROMPT
    context = MARKDOWN_CONTEXT_PROMPT + "1. 개인신용정보란 금융거래 등 상거래에서 개인인 정보주체의 신용, 거래내용, 거래능력 등을 판단할 수 있는 정보를 뜻한다"
    query = "개인신용정보가 무엇인가요?"
    result = await chain.invoke(system_message, context, query)
    assert isinstance(result, str) and len(result) > 0

@pytest.mark.asyncio
async def test_invoke_with_long_chat_history():
    system_message = MARKDOWN_QUERY_SYSTEM_PROMPT
    context = MARKDOWN_CONTEXT_PROMPT + "1. 개인신용정보란 금융거래 등 상거래에서 개인인 정보주체의 신용, 거래내용, 거래능력 등을 판단할 수 있는 정보를 뜻한다"
    query = "개인신용정보가 무엇인가요?"
    chat_history = [("user", f"방금 말 영어로 해줘") for i in range(1, chain.get_model_token_limit() // 10)]    # "방금 말 영어로 해줘"의 토큰 사이즈가 13
    result = await chain.invoke(system_message, context, query, chat_history)
    assert isinstance(result, str) and len(result) > 0
