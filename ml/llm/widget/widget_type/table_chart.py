from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from schemas.base import CamelizedBaseModel


class LLMTableWidget(CamelizedBaseModel):
    title: str = Field(description='название бейджа')
    data: int | float = Field(description='значение внутри бейджа')


badge_widget_info = {
    'name': 'table',
    'description': 'Наиболее подходящий виджет для отображения значимой цифры (например, средняя зарплата в компании)',
    'parser': PydanticOutputParser(pydantic_object=LLMTableWidget),
}
