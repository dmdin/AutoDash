from fastapi import (
    APIRouter, WebSocket
)
from ..dependencies import container
from schemas.message import ChatResponseTemplateGenerator, TemplateGeneratorInput
from langchain.schema import BaseMessage

router = APIRouter(prefix='/llm')


@router.websocket(
    '/generate_template',
)
async def generate_template(websocket: WebSocket) -> ChatResponseTemplateGenerator:
    """
    Returns all documents suitable for RAG
    """
    await websocket.accept()
    raw_data = await websocket.receive_json()
    data = TemplateGeneratorInput(input_theme=raw_data['input_theme'], model_name=raw_data['model_name'])
    template: BaseMessage
    async for template in container.openai_supplier.generate_template(data.input_theme, data.model_name):
        response = ChatResponseTemplateGenerator(message=template.content)
        await websocket.send_json(response.json())
