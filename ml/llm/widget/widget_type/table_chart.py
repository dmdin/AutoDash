from langchain.output_parsers import PydanticOutputParser
from pydantic import Field, validator

from schemas.base import CamelizedBaseModel


class LLMTableRowWidget(CamelizedBaseModel):
    data: list[str | int | float] = Field(
        description='отдельная строка таблицы, каждый элемент должен соответствовать заголовку, каждый элемент представляет из себя единицу информации, которая указана в заголовке'
    )


class LLMTableWidget(CamelizedBaseModel):
    categories: list[str] = Field(description='строка загаловка таблицы')
    rows: list[LLMTableRowWidget] = Field(
        description='массив строк таблицы, каждая строка должна совпадать по длине со строкой заголовка'
    )

    @validator('rows')
    def lengths_rows_data_categories_match(cls, v, values, **kwargs):
        if 'categories' in values:
            for _v in v:
                if len(_v) != len(values['categories']):
                    raise ValueError(
                        "data's row and categories are of different length"
                    )
        return v


table_widget_info = {
    'name': 'table',
    'description': 'Лучший для большого количества разной информации (например, сводная таблица по разным компаниям)',
    'parser': PydanticOutputParser(pydantic_object=LLMTableWidget),
}
