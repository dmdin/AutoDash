from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from schemas.base import CamelizedBaseModel


class LLMBadgeWidget(CamelizedBaseModel):
    title: str = Field(description='название бейджа')
    data: int | float = Field(description='значение внутри бейджа')


badge_widget_info = (
    {
        'name': 'badge',
        'description': 'Наиболее подходящий виджет для отображения значимой цифры (например, средняя зарплата в компании)',
        'parser': PydanticOutputParser(LLMBadgeWidget),
    },
)
