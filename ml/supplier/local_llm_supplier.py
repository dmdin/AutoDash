from dataclasses import dataclass
from enum import Enum

from langchain_huggingface import HuggingFaceEmbeddings

from shared.settings import app_settings


class LOCAL_LLM_EMBEDDING_MODELS(str, Enum):
    RUBERT_TINY2 = 'rubert-tiny2'


@dataclass
class LocalLLMSupplier:
    def __post_init__(self):
        assert app_settings.local_llm_embedding_model_name
        self.embeddings: HuggingFaceEmbeddings = HuggingFaceEmbeddings(
            model_name=app_settings.local_llm_embedding_model_name
        )

    async def health(self) -> None:
        assert self.embeddings
