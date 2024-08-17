from enum import Enum

class VectorStoreType(str, Enum):
    FAISS = "FaissStore"

class LargeLanguageModelType(str, Enum):
    OPENAI = "OpenaiChain"
