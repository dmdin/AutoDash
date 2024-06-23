from dataclasses import dataclass

import httpx
from langchain.docstore.document import Document

from schemas.search_parser import SearchParsedDocumentList
from shared.base import logger
from shared.settings import app_settings


@dataclass
class SearchSupplier:
    def __post_init__(self):
        self.host = app_settings.search_host
        self.port = app_settings.search_port

    @property
    def search_data_for_llm_route(self):
        return f'http://{self.host}:{self.port}/search_data_for_llm_v2'

    async def health(self):
        if not httpx.get(f'http://{self.host}:{self.port}/ping'):
            raise Exception('non true ping')

    async def search_data_for_llm(self, query: str, urls: list[str] | None):
        if not urls:
            urls = []
        async with httpx.AsyncClient() as client:
            try:
                data = {
                    'query': query,
                    'urls': urls,
                }
                response: httpx.Response = await client.post(
                    self.search_data_for_llm_route,
                    json=data,
                )
                print(response.json())
                all_documents: SearchParsedDocumentList = SearchParsedDocumentList(
                    **response.json()
                )
            except httpx.HTTPError as e:
                logger.debug(e)
                all_documents: SearchParsedDocumentList = SearchParsedDocumentList(
                    results=[], errors=[]
                )
            return all_documents

    def parse_documents_from_search(
        self, documents: SearchParsedDocumentList
    ) -> list[Document]:
        langchain_documents: list[Document] = []
        for doc in documents.results:
            try:
                new_doc = Document(
                    doc.text,
                    page_title=doc.title,
                    url=doc.url,
                )
                langchain_documents.append(new_doc)
            except Exception as e:
                logger.debug(e)
                continue
        return langchain_documents
