import os
import shutil
import pytest
from app.vector_store.faiss import FaissStore
from utils.key_conf import KEY_CONF
from utils.exception import InitializationException

faiss = FaissStore()
initialized_success = False

@pytest.mark.run(order=1)
@pytest.mark.asyncio
async def test_not_initialized():
    try:
        await faiss.retrieve("test")
    except InitializationException as e:
        assert str(e) == "Vector store initialization work does not started!"
        try:
            await faiss.initialize(
                KEY_CONF.TEST_DATA_PATH,
                'pdf',
                KEY_CONF.EMBEDDING_MODEL,
                KEY_CONF.CHUNK_SIZE,
                KEY_CONF.CHUNK_OVERLAP
            )
        except Exception as e:
            print(e)
        else:
            initialized_success = True
            assert True
    else:
        pytest.fail("Expected InitializationException was not raised")

@pytest.mark.skipif(initialized_success, reason="initialized fail")
@pytest.mark.asyncio
async def test_create_store():
    test_embedding_folder = KEY_CONF.TEST_DATA_PATH + '/faiss'
    if os.path.exists(test_embedding_folder):
        shutil.rmtree(test_embedding_folder)
    try:
        await faiss.initialize(
            KEY_CONF.TEST_DATA_PATH,
            'pdf',
            KEY_CONF.EMBEDDING_MODEL,
            KEY_CONF.CHUNK_SIZE,
            KEY_CONF.CHUNK_OVERLAP
        )
    except Exception as e:
        print(e)
        initialized_success = False
        assert False
    else:
        assert faiss.get_vector_store() is not None

@pytest.mark.skipif(initialized_success, reason="initialized fail")
@pytest.mark.asyncio
async def test_load_store():
    try:
        await faiss.initialize(
            KEY_CONF.TEST_DATA_PATH,
            'pdf',
            KEY_CONF.EMBEDDING_MODEL,
            KEY_CONF.CHUNK_SIZE,
            KEY_CONF.CHUNK_OVERLAP
        )
    except Exception as e:
        print(e)
        initialized_success = False
        assert False
    else:
        assert faiss.get_vector_store() is not None

@pytest.mark.skipif(initialized_success, reason="initialized fail")
@pytest.mark.asyncio
async def test_retrieve():
    try:
        context_list = await faiss.retrieve("개인신용정보가 뭐야?")
    except Exception as e:
        print(e)
        assert False
    else:
        assert len(context_list) > 0
