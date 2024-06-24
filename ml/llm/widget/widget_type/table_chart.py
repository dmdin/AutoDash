from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from schemas.base import CamelizedBaseModel


class LLMTableWidget(CamelizedBaseModel):
    categories: list[str] = Field(description='строка загаловка таблицы')
    rows: list[list[str | int | float]] = Field(
        description='матрица значений таблицы, количество столбцов должно совпадать с длиной строки заголовока'
    )


table_widget_info = {
    'name': 'table',
    'description': 'Лучший для большого количества разной информации',
    'parser': PydanticOutputParser(pydantic_object=LLMTableWidget),
}
