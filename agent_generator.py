from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
import asyncio
from typing import *
from agent import init_agent
from langchain.schema import LLMResult

class Handler(AsyncIteratorCallbackHandler):

    def __init__(self) -> None:
        super().__init__()
        self.received_tokens = False

    async def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        await super().on_llm_start(serialized, prompts, **kwargs)
        print("start")

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        if token is not None and token != "":
            self.received_tokens = True
            self.queue.put_nowait(token)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        if self.received_tokens:
            self.done.set()

async def run_agent(question, session_id):
    handler = Handler()
    agent = init_agent(handler, session_id)
    task = asyncio.create_task(agent.acall({"question": question}))
    async for token in handler.aiter():
        print(token)
        yield token
    await task