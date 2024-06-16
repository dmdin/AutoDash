from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from service.health_service import HealthService
from supplier.openapi_supplier import OpenAISupplier


@dataclass
class Container:
    heath_service: HealthService
    redis_repository: RedisRepository
    openai_supplier: OpenAISupplier


def init_combat_container() -> Container:
    redis_repository = RedisRepository()
    heath_service = HealthService(redis_repository=redis_repository)
    openai_supplier = OpenAISupplier()

    return Container(
        heath_service=heath_service,
        redis_repository=redis_repository,
        openai_supplier=openai_supplier,
    )
