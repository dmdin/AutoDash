from dataclasses import dataclass

import httpx
from langchain.docstore.document import Document

from schemas.search_parser import SearchParsedDocument, SearchParsedSourceDocuments
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

    async def search_data_for_llm(self, query: str, urls: SearchParsedSourceDocuments):
        async with httpx.AsyncClient() as client:
            try:
                data = {
                    'query': query,
                    'urls': urls.urls,
                    'return_html': False,
                    'extra_data': False,
                }
                response: httpx.Response = await client.post(
                    self.search_data_for_llm_route,
                    data=data,
                )
                all_documents: list[SearchParsedDocument] = response.json()
            except httpx.HTTPError as e:
                logger.debug(e)
                all_documents: list[SearchParsedDocument] = []
            return all_documents

    def parse_documents_from_search(
        self, documents: list[SearchParsedDocument]
    ) -> list[Document]:
        langchain_documents: list[Document] = []
        for doc in documents:
            try:
                new_doc = Document(
                    doc['all_text_from_page'],
                    page_title=doc['page_title'],
                    url=doc['url'],
                )
                langchain_documents.append(new_doc)
            except Exception as e:
                logger.debug(e)
                continue
        return langchain_documents
