from langchain.output_parsers import PydanticOutputParser
from pydantic import Field, validator

from schemas.base import CamelizedBaseModel


class LLMBarWidget(CamelizedBaseModel):
    title: str = Field(description='название гистограммы')
    categories: list[str] = Field(description='здесь указаны метки оси X')
    unit: str = Field(
        description='единица измерения (все данные должны соответсвовать выбранной единице измерения)'
    )
    data: list[int | float] = Field(description='значения для каждой точки')

    @validator('data')
    def lengths_data_categories_match(cls, v, values, **kwargs):
        if 'categories' in values and len(v) != len(values['categories']):
            raise ValueError('data and categories are of different length')
        return v


bar_widget_info = {
    'name': 'bar',
    'description': 'Наиболее подходящий виджет для отображения относительных показателей между разными компаниями',
    'parser': PydanticOutputParser(pydantic_object=LLMBarWidget),
}
