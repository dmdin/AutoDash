from langchain.output_parsers import PydanticOutputParser
from pydantic import Field, validator

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
        description='массив всех частей круговой диаграммы (должно быть как минимум две части)'
    )

    @validator('data')
    def data_must_containt_more_pieces(cls, v):
        if len(v) < 2:
            raise ValueError('data contains only one pie piece')
        return v


pie_widget_info = {
    'name': 'pie',
    'description': 'Наиболее подходящий виджет для отображения долей (например, доля каждой компании на рынке, или доля мужчин и женщин в компании)',
    'parser': PydanticOutputParser(pydantic_object=LLMPieWidget),
}
