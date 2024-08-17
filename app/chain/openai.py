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
    
    def _make_chain(self, system_message: str, context: str, chat_history:list = []):
        messages = list()
        messages.append(("system", system_message))
        messages.append(("system", context))
        messages.extend(chat_history)
        messages.append(("user", "{user_input}"))
        prompt = ChatPromptTemplate.from_messages(messages)
        llm = ChatOpenAI(model = self.model_name, temperature = self.temperature)
        chain = prompt | llm | StrOutputParser()
        return chain

    
    async def invoke(self, system_message: str, context: str, query: str, chat_history:list = []):
        chain = self._make_chain(system_message, context, chat_history)
        log.info(f"invoke with query: {query}")
        result = await chain.ainvoke({"user_input": query})
        return result
