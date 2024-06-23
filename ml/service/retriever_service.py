from dataclasses import dataclass
from typing import Optional

from langchain.retrievers import ParentDocumentRetriever
from langchain.storage._lc_store import create_kv_docstore
from langchain_chroma import Chroma
from langchain_community.storage import RedisStore
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter


@dataclass
class RetrieverService:
    vectorstore: Chroma
    store: RedisStore
    child_splitter: Optional[TextSplitter] = None
    parent_splitter: Optional[TextSplitter] = None
    use_parent_splitter: bool = True

    def __post_init__(self):
        self.base_child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, chunk_overlap=64
        )
        self.base_parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048, chunk_overlap=256
        )
        if not self.child_splitter:
            self.child_splitter = self.base_child_splitter
        if not self.parent_splitter and self.use_parent_splitter:
            self.parent_splitter = self.base_parent_splitter
        byte_docstore = create_kv_docstore(
            self.store
        )  # required for RedisStore to be used

        self.retriever = ParentDocumentRetriever(
            vectorstore=self.vectorstore,
            docstore=byte_docstore,
            child_splitter=self.child_splitter,
            parent_splitter=self.parent_splitter,
        )
