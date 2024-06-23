from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from schemas.base import CamelizedBaseModel


class LLMPiePiece(CamelizedBaseModel):
    name: str = Field(description='название части круговой диаграммы')
    value: int | float = Field(description='значение части кругово диаграммы')


class LLMPieWidget(CamelizedBaseModel):
    title: str = Field(description='название круговой диаграммы')
    unit: str = Field(
        description='единица измерения (все данные должны соответсвовать выбранной единице измерения)'
    )
    data: list[LLMPiePiece] = Field(
        description='массив всех частей круговой диаграммы (должно быть как минимум две части)',
        min_items=2,
    )


pie_widget_info = {
    'name': 'pie',
    'description': 'Наиболее подходящий виджет для отображения долей',
    'parser': PydanticOutputParser(pydantic_object=LLMPieWidget),
}
