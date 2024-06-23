import random
from time import time

import ujson as json
from langchain.output_parsers import PydanticOutputParser, RetryWithErrorOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain.pydantic_v1 import ValidationError

from schemas.report_template import (
    ReportTemplateGeneratorInput,
    ReportTemplateParserInput,
)
from shared.base import logger
from shared.containers import Container

from .model import ReportTemplate, ReportTemplateBlock
from .templates import template, template_parser, template_w_examples


async def generate_template(
    container: Container,
    input_data: ReportTemplateGeneratorInput,
    use_template_w_examples: bool = False,
    n_blocks: int = -1,
):
    logging_time_start = time()
    if n_blocks == -1:
        n_blocks = random.randint(5, 8)

    chat_model = container.openai_supplier.get_model(input_data.model_name)
    parser = PydanticOutputParser(pydantic_object=ReportTemplateBlock)
    parser_fixer = RetryWithErrorOutputParser.from_llm(
        llm=chat_model, parser=parser, max_retries=10
    )

    if use_template_w_examples:
        block_examples = [
            json.dumps(x) for x in container.openai_supplier.block_examples
        ]
        block_examples_str = '\n'.join(block_examples)
        chat_template = template_w_examples
        prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
            chat_template
        ).partial(
            input_theme=input_data.input_theme,
            format_instructions=parser.get_format_instructions(),
            block_examples=block_examples_str,
        )
    else:
        chat_template = template
        prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
            chat_template
        ).partial(
            input_theme=input_data.input_theme,
            format_instructions=parser.get_format_instructions(),
        )

    history_blocks = ''
    for block in range(n_blocks):
        logging_block_time_start = time()
        n_points = random.randint(1, 8)
        completion_chain = prompt | chat_model
        response = await completion_chain.ainvoke({
            'input': f'Сформируй блок номер {block + 1} состоящий из {n_points} пунктов',
            'history_blocks': history_blocks,
        })
        try:
            parsed_response = await parser.aparse(response)
        except ValidationError as e:
            logger.debug(f'Error occured while parsing: {e}')
            parsed_response = await parser_fixer.aparse_with_prompt(
                completion=response.content, prompt_value=prompt
            )
        history_blocks = history_blocks + '\n' + str(parsed_response)
        yield parsed_response
        logger.debug(
            f'Time for single block generation: {time() - logging_block_time_start}'
        )
    logger.debug(
        f'Time for the full template generation: {time() - logging_time_start}'
    )


async def parse_template(
    container: Container, input_data: ReportTemplateParserInput
) -> ReportTemplate:
    logging_time_start = time()
    parser = PydanticOutputParser(pydantic_object=ReportTemplate)
    chat_template = template_parser
    chat_model = container.openai_supplier.get_model(input_data.model_name)
    parser_fixer = RetryWithErrorOutputParser.from_llm(
        llm=chat_model, parser=parser, max_retries=10
    )
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(chat_template)
    completion_chain = prompt | chat_model
    input_kwargs = {
        'input_theme': input_data.input_theme,
        'format_instructions': parser.get_format_instructions(),
        'raw_report_template_text': input_data.raw_report_template_text,
    }
    response = await completion_chain.ainvoke(input_kwargs)
    try:
        parsed_response = await parser.aparse(response)
    except ValidationError as e:
        logger.debug(f'Error occured while parsing: {e}')
        parsed_response = await parser_fixer.aparse_with_prompt(
            completion=response.content,
            prompt_value=prompt.format_prompt(**input_kwargs),
        )
    logger.debug(f'Time for the full template parsing: {time() - logging_time_start}')
    return parsed_response
