from dataclasses import dataclass

import chromadb
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings

from shared.settings import app_settings


@dataclass
class ChromaRepository:
    def __post_init__(self) -> None:
        self.client = chromadb.HttpClient(
            host=app_settings.chroma_host, port=app_settings.chroma_port
        )
        self.collection_name = 'vectorstore_collection'
        self.langchain_chroma = None

    async def health(self) -> None:
        if not self.client.heartbeat():
            raise Exception('non true ping')

    def setup_langchain_chroma(self, embedding_function: Embeddings):
        self.langchain_chroma = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=embedding_function,
            create_collection_if_not_exists=True,
        )

    def get_langchain_chroma(self):
        if self.langchain_chroma:
            return self.langchain_chroma
        else:
            raise AttributeError('No langchain chroma connector found, try setup first')
