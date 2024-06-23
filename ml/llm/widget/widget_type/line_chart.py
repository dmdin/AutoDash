from langchain.output_parsers import PydanticOutputParser
from pydantic import Field, validator

from schemas.base import CamelizedBaseModel


class LLMLineWidget(CamelizedBaseModel):
    title: str = Field(description='название линейного графика')
    categories: list[str] = Field(
        description='здесь указаны метки оси X (зачастую, это ось времени, например, года или дни)'
    )
    unit: str = Field(
        description='единица измерения (все данные должны соответсвовать выбранной единице измерения)'
    )
    data: list[int | float] = Field(description='значения для каждой точки')

    @validator('data')
    def lengths_data_categories_match(cls, v, values, **kwargs):
        if 'categories' in values and len(v) != len(values['categories']):
            raise ValueError('data and categories are of different length')
        return v


line_widget_info = {
    'name': 'line',
    'description': 'Наиболее подходящий виджет для отображения временных изменений (например, график изменения средней зарплаты в компании)',
    'parser': PydanticOutputParser(pydantic_object=LLMLineWidget),
}
