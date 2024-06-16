from typing import Any

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler

from schemas.message import ChatResponseTemplateGenerator

class StreamingLLMCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming LLM responses."""

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def on_llm_new_token_template_generator(self, token: str, **kwargs: Any) -> None:
        resp = ChatResponseTemplateGenerator(message=token)
        await self.websocket.send_json(resp.json())
