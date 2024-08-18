import tiktoken
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from chain.abstract_chain import ChainModel, log
from utils.key_conf import KEY_CONF

class OpenaiChain(ChainModel):
    def __init__(self, model_name: str = KEY_CONF.DEFAULT_OPENAI_MODEL, temperature: int = 0):
        super().__init__()
        self.model_name = model_name
        self.temperature = temperature
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            log.warning("Warning: model not found. Using cl100k_base encoding.")
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def num_tokens_from_message(self, message: str):
        tokens_per_message = 3
        num_tokens = 0
        num_tokens += tokens_per_message
        num_tokens += len(self.encoding.encode(message))
        return num_tokens

    def total_tokens_from_messages(self, messages: list) -> int :
        tokens_per_message = 3
        num_tokens = 0
        for role, message in messages:
            num_tokens += tokens_per_message
            num_tokens += len(self.encoding.encode(role))
            num_tokens += len(self.encoding.encode(message))
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
    
    def _make_chain(self, system_message: str, context: str, query: str, chat_history:list = []):
        model_token_limit = self.get_model_token_limit()
        query_token_num =self.num_tokens_from_message(query)
        messages = list()
        messages.append(("system", system_message))
        messages.append(("system", context))
        messages.extend(chat_history)
        while self.total_tokens_from_messages(messages) > model_token_limit - query_token_num - 100: # not too tight token limit
            chat_history.pop(0)
            messages = list()
            messages.append(("system", system_message))
            messages.append(("system", context))
            messages.extend(chat_history)
        messages.append(("user", "{user_input}"))
        prompt = ChatPromptTemplate.from_messages(messages)
        llm = ChatOpenAI(model = self.model_name, temperature = self.temperature)
        chain = prompt | llm | StrOutputParser()
        return chain
    
    def get_model_token_limit(self):
        if self.model_name == 'gpt-3.5-turbo-instruct':
            return 4096
        elif 'gpt-3.5-turbo' in self.model_name:
            return 16385
        elif 'gpt-4-turbo' in self.model_name or self.model_name == 'gpt-4-1106-preview':
            return 128000
        elif 'gpt-4o' in self.model_name:
            return 128000
        elif 'gpt-4' in self.model_name:
            return 8192
        else:
            log.warning("Warning: model not found. Using minimum token limit.")
            return 4096

    async def invoke(self, system_message: str, context: str, query: str, chat_history:list = []):
        chain = self._make_chain(system_message, context, query, chat_history)
        log.info(f"invoke with query: {query}")
        result = await chain.ainvoke({"user_input": query})
        return result
