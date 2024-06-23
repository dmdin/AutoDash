import random

import ujson as json
from langchain.chains.llm import LLMChain
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
)

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

    chat_model = container.openai_supplier.get_model(input_data.model_name)
    parser = PydanticOutputParser(pydantic_object=ReportTemplateBlock)
    parser_fixer = OutputFixingParser.from_llm(llm=chat_model, parser=parser)

    if use_template_w_examples:
        block_examples = [
            json.dumps(x) for x in container.openai_supplier.block_examples
        ]
        block_examples_str = '\n'.join(block_examples)
        chat_template = template_w_examples
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
            chat_template
        ).partial(
            input_theme=input_data.input_theme,
            format_instructions=parser.get_format_instructions(),
            block_examples=block_examples_str,
        )
    else:
        chat_template = template
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
            chat_template
        ).partial(
            input_theme=input_data.input_theme,
            format_instructions=parser.get_format_instructions(),
        )

    history_blocks = ''
    for block in range(n_blocks):
        n_points = random.randint(1, 8)
        chain = prompt_template | chat_model | parser_fixer
        response = await chain.ainvoke({
            'input': f'Сформируй блок номер {block + 1} состоящий из {n_points} пунктов',
            'history_blocks': history_blocks,
        })
        history_blocks = history_blocks + '\n' + str(response)
        yield response


async def parse_template(container: Container, input_data: ReportTemplateParserInput):
    parser = PydanticOutputParser(pydantic_object=ReportTemplate)
    chat_template = template_parser
    chat_model = container.openai_supplier.get_model(input_data.model_name)
    parser_fixer = OutputFixingParser.from_llm(llm=chat_model, parser=parser)
    prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        chat_template
    )
    chain: LLMChain = prompt_template | chat_model | parser_fixer
    response: ReportTemplate = await chain.ainvoke({
        'input_theme': input_data.input_theme,
        'format_instructions': parser.get_format_instructions(),
        'raw_report_template_text': input_data.raw_report_template_text,
    })
    return response
