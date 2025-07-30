from mirascope import BaseMessageParam, llm

LLM = None

def dynLLM(*messages: list[BaseMessageParam]):
    return LLM(lambda: list(messages))()