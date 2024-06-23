import random

import ujson as json
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate

from schemas.report_template import (
    ReportTemplateGeneratorInput,
    ReportTemplateParserInput,
)
from shared.containers import Container

from .model import ReportTemplate, ReportTemplateBlock
from .templates import template, template_parser, template_w_examples


async def generate_template(
    container: Container,
    input_data: ReportTemplateGeneratorInput,
    use_template_w_examples: bool = False,
    n_blocks: int = -1,
):
    if n_blocks == -1:
        n_blocks = random.randint(5, 8)

    memory = ConversationBufferMemory()
    parser = PydanticOutputParser(ReportTemplateBlock)

    if use_template_w_examples:
        chat_template = template_w_examples
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
            chat_template
        )
        block_examples = [
            json.dumps(x) for x in container.openai_supplier.block_examples
        ]
        block_examples_str = '\n'.join(block_examples)
        prompt = prompt_template.format_messages(
            input_theme=input_data.input_theme,
            block_examples=block_examples_str,
            format_instructions=parser.get_format_instructions(),
        )
    else:
        chat_template = template
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
            chat_template
        )
        prompt = prompt_template.format_messages(
            input_theme=input_data.input_theme,
            format_instructions=parser.get_format_instructions(),
        )

    chain = ConversationChain(
        llm=container.openai_supplier.get_model(input_data.model_name),
        memory=memory,
        prompt=prompt,
        output_parser=parser,
    )
    for block in range(n_blocks):
        n_points = random.randint(1, 8)
        response = await chain.ainvoke({
            'input': f'Сформируй блок номер {block + 1} состоящий из {n_points} пунктов!'
        })
        yield response


async def parse_template(container: Container, input_data: ReportTemplateParserInput):
    parser = PydanticOutputParser(ReportTemplate)
    chat_template = template_parser
    prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        chat_template
    )
    chain: LLMChain = (
        prompt_template
        | container.openai_supplier.get_model(input_data.model_name)
        | parser
    )
    response = await chain.ainvoke({
        'input_theme': input_data.input_theme,
        'format_instructions': parser.get_format_instructions(),
        'raw_report_template_text': input_data.raw_report_template_text,
    })
    return response
