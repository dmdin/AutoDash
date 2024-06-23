from pydantic import Field

from schemas.base import CamelizedBaseModel


class ReportTemplateBlock(CamelizedBaseModel):
    block_name: str = Field(
        description='название блока, обычно выглядит в формате "Блок номер_блока: тематика_блока"'
    )
    points: list[str] = Field(description='пункты в блоке')


class ReportTemplate(CamelizedBaseModel):
    blocks: list[ReportTemplateBlock] = Field(description='блоки в шаблоне')
