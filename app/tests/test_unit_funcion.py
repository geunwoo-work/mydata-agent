import pytest
from vector_store import VECTOR_STORES
from chain import CHAIN_STORES
from utils.key_conf import KEY_CONF
from utils.enums import LargeLanguageModelType, VectorStoreType
from prompt.en import MARKDOWN_QUERY_SYSTEM_PROMPT, MARKDOWN_CONTEXT_PROMPT
from routers.v1.chatrooms import summarize_context

faiss = VECTOR_STORES[VectorStoreType.FAISS]
chain = CHAIN_STORES[LargeLanguageModelType.OPENAI]

@pytest.mark.asyncio
async def test_summarize_context():
    await faiss.initialize(
        KEY_CONF.TEST_DATA_PATH,
        'pdf',
        KEY_CONF.EMBEDDING_MODEL,
        KEY_CONF.CHUNK_SIZE,
        KEY_CONF.CHUNK_OVERLAP
    )
    chain.set_model_name(KEY_CONF.DEFAULT_OPENAI_MODEL)
    query = "개인신용정보가 뭐야?"
    context_list = await faiss.retrieve("개인신용정보가 뭐야?")
    multiple_context_list = [context * 10 for context in context_list]
    summarized_context_list = await summarize_context(chain, multiple_context_list, query)
    assert len(context_list) == len(summarized_context_list)
    for idx, multiple_context in enumerate(multiple_context_list):
        assert chain.num_tokens_from_message(multiple_context) > \
                chain.num_tokens_from_message(summarized_context_list[idx])
