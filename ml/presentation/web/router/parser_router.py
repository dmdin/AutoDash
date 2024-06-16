from fastapi import (
    APIRouter,
)
import httpx
from schemas.parser import ParserDocument, SourceDocuments
from shared.settings import app_settings

router = APIRouter(prefix='/parser')


@router.post(
    '/get_data_for_llm',
    response_model=list[ParserDocument],
    response_model_exclude_defaults=True,
    response_model_exclude_none=True,
)
async def get_data_for_llm(query: str, urls: SourceDocuments) -> list[ParserDocument]:
    """
    Returns all documents suitable for RAG
    """
    api_url = (
        f'{app_settings.parser_host}:{app_settings.parser_port}/search_data_for_llm'
    )
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(api_url, params={"query": query}, data=urls.json())
        all_documents: list[ParserDocument] = response.json()
        return all_documents
