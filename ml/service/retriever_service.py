from dataclasses import dataclass
from typing import Optional

from langchain.retrievers import ParentDocumentRetriever
from langchain.storage._lc_store import create_kv_docstore
from langchain_chroma import Chroma
from langchain_community.storage import RedisStore
from langchain_text_splitters import (
    CharacterTextSplitter,
    TextSplitter,
)


@dataclass
class RetrieverService:
    vectorstore: Chroma
    store: RedisStore
    child_splitter: Optional[TextSplitter] = None
    parent_splitter: Optional[TextSplitter] = None
    use_parent_splitter: bool = True

    def __post_init__(self):
        self.base_child_splitter = CharacterTextSplitter(chunk_size=64, chunk_overlap=4)
        self.base_parent_splitter = CharacterTextSplitter(
            chunk_size=256, chunk_overlap=16
        )
        # if not self.child_splitter:
        # self.child_splitter = self.base_child_splitter
        # if not self.parent_splitter and self.use_parent_splitter:
        # self.parent_splitter = self.base_parent_splitter
        self.byte_docstore = create_kv_docstore(
            self.store
        )  # required for RedisStore to be used

        self.child_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            model_name='gpt-4o',
            chunk_size=32,
            chunk_overlap=0,
        )
        self.parent_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            model_name='gpt-4o',
            chunk_size=128,
            chunk_overlap=8,
        )

        self.retriever = ParentDocumentRetriever(
            vectorstore=self.vectorstore,
            docstore=self.byte_docstore,
            child_splitter=self.child_splitter,
            parent_splitter=self.parent_splitter,
            search_kwargs={'k': 2},
        )

    def recreate_retriever_with_context(self, vectorstore: Chroma):
        self.retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=self.byte_docstore,
            child_splitter=self.child_splitter,
            parent_splitter=self.parent_splitter,
            search_kwargs={'k': 2},
        )
        return self.retriever

    async def health(self) -> None:
        try:
            if self.retriever is not None:
                pass
            else:
                raise AttributeError(
                    'retriever is empty? a problem has occured somewhere'
                )
        except AttributeError as e:
            raise e
