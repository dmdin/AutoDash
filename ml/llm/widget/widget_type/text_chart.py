from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from schemas.base import CamelizedBaseModel


class LLMTextWidget(CamelizedBaseModel):
    title: str = Field(description='заголовок')
    text: str = Field(description='основное тело текста')


text_widget_info = {
    'name': 'text',
    'description': 'Наиболее подходящий виджет для отображения текстовой информации, ЛУЧШЕ НЕ ИСПОЛЬЗОВАТЬ ВООБЩЕ',
    'parser': PydanticOutputParser(pydantic_object=LLMTextWidget),
}
