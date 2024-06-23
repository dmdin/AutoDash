from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from schemas.base import CamelizedBaseModel


class LLMTextWidget(CamelizedBaseModel):
    title: str = Field(description='заголовок')
    text: str = Field(description='основное тело текста')


text_widget_info = (
    {
        'name': 'pie',
        'description': 'Наиболее подходящий виджет для отображения текстовой информации (например, когда необходимо сформировать вывод по проанализированной информации)',
        'parser': PydanticOutputParser(LLMTextWidget),
    },
)
