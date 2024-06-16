from fastapi import (
    APIRouter, WebSocket
)
from ..dependencies import container
from schemas.message import ChatResponseTemplateGenerator
from langchain.schema import BaseMessage

router = APIRouter(prefix='/llm')


@router.websocket(
    '/generate_template',
)
async def generate_template(websocket: WebSocket, input_theme: str, model_name: str) -> ChatResponseTemplateGenerator:
    """
    Returns all documents suitable for RAG
    """
    await websocket.accept()
    while True:
        template: BaseMessage = await container.openai_supplier.generate_template(input_theme, model_name)
        response = ChatResponseTemplateGenerator(template.content)
        await websocket.send_json(response.json())
