from dataclasses import dataclass

from service.health_service import HealthService
from supplier.openapi_supplier import OpenAISupplier


@dataclass
class Container:
    heath_service: HealthService
    openai_supplier: OpenAISupplier


def init_combat_container() -> Container:
    heath_service = HealthService()
    openai_supplier = OpenAISupplier()

    return Container(
        heath_service=heath_service,
        openai_supplier=openai_supplier,
    )
