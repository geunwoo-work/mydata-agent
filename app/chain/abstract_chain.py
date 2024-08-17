from abc import ABC, abstractmethod
from conf.log_conf import loggers

log = loggers['chain']

class ChainModel(ABC):
    def __init__(self, model_name):
        self.model_name = model_name
        pass

    @abstractmethod
    async def invoke(self, context, query):
        pass
