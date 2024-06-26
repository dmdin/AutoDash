from dataclasses import dataclass
from enum import Enum

from langchain_huggingface import HuggingFaceEmbeddings

from shared.settings import app_settings


class LOCAL_LLM_EMBEDDING_MODELS(str, Enum):
    RUBERT_TINY2 = 'cointegrated/rubert-tiny2'


@dataclass
class LocalLLMSupplier:
    def __post_init__(self):
        self.embeddings: HuggingFaceEmbeddings = HuggingFaceEmbeddings(
            model_name='.'.join(app_settings.embedding_model.split('.')[1:])
        )

    async def health(self) -> None:
        assert self.embeddings
