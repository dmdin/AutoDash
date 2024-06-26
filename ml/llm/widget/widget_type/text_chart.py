from langchain.output_parsers import PydanticOutputParser
from pydantic import Field

from schemas.base import CamelizedBaseModel


class LLMTextWidget(CamelizedBaseModel):
    title: str = Field(description='заголовок')
    text: str = Field(description='основное тело текста')


text_widget_info = {
    'name': 'text',
    'description': 'Для текста',
    'parser': PydanticOutputParser(pydantic_object=LLMTextWidget),
}
