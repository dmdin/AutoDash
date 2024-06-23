from dataclasses import dataclass

from repository.chroma_repository import ChromaRepository
from repository.redis_repository import RedisRepository
from service.retriever_service import RetrieverService
from supplier.local_llm_supplier import LocalLLMSupplier
from supplier.openapi_supplier import OpenAISupplier
from supplier.search_supplier import SearchSupplier


@dataclass
class Container:
    chroma_repository: ChromaRepository
    openai_supplier: OpenAISupplier
    redis_repository: RedisRepository
    retriever_service: RetrieverService
    local_llm_supplier: LocalLLMSupplier
    search_supplier: SearchSupplier


def init_combat_container() -> Container:
    chroma_repository = ChromaRepository()
    redis_repository = RedisRepository()
    openai_supplier = OpenAISupplier()
    search_supplier = SearchSupplier()
    local_llm_supplier = LocalLLMSupplier()
    try:
        chroma_store = chroma_repository.get_langchain_chroma()
    except AttributeError:
        # chroma_repository.setup_langchain_chroma(openai_supplier.embeddings)
        chroma_repository.setup_langchain_chroma(local_llm_supplier.embeddings)
        chroma_store = chroma_repository.get_langchain_chroma()
    retriever_service = RetrieverService(chroma_store, redis_repository.rs)

    return Container(
        chroma_repository=chroma_repository,
        local_llm_supplier=local_llm_supplier,
        openai_supplier=openai_supplier,
        redis_repository=redis_repository,
        retriever_service=retriever_service,
        search_supplier=search_supplier,
    )
