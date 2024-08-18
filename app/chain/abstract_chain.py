import tiktoken
from abc import ABC, abstractmethod
from conf.log_conf import loggers

log = loggers['chain']

class ChainModel(ABC):
    def __init__(self):
        self.model_name = ""

    def set_model_name(self, model_name: str):
        self.model_name = model_name
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            log.warning("Warning: model not found. Using cl100k_base encoding.")
            self.encoding = tiktoken.get_encoding("cl100k_base")

    @abstractmethod
    def num_tokens_from_message(message: str):
        pass

    @abstractmethod
    def get_model_token_limit():
        pass

    @abstractmethod
    async def invoke(self, context: str, query: str):
        pass
