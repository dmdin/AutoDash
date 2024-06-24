from functools import partial
from typing import Callable

from langchain.chains.llm import LLMChain
from langchain.output_parsers import PydanticOutputParser, RetryOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import ValidationError
from langchain_core.messages import BaseMessage

from schemas.report_widget import ParsedReportGeneratorInput, WidgetChartType
from shared.base import logger
from shared.containers import Container

from .model import LLMWidgetType
from .templates import router_template, widget_template
from .widget_type import all_widget_types


async def create_chain_function(
    completion_chain: LLMChain,
    prompt: ChatPromptTemplate,
    parser: PydanticOutputParser,
    parser_fixer: RetryOutputParser,
    input_kwargs: dict[str, str],
):
    response: BaseMessage = await completion_chain.ainvoke(input_kwargs)
    try:
        parsed_response = await parser.aparse(response)
    except ValidationError as e:
        logger.debug(f'Error occured while parsing: {e}')
        try:
            parsed_response = await parser_fixer.aparse_with_prompt(
                completion=response.content,
                prompt_value=prompt.format_prompt(**input_kwargs),
            )
        except Exception as e:
            logger.debug(e)
            return None
    return parsed_response


def generate_destinations(
    container: Container, input_data: ParsedReportGeneratorInput
) -> dict[WidgetChartType, Callable]:
    destination_chains: dict[WidgetChartType, LLMChain] = {}
    chat_model = container.openai_supplier.get_model(input_data.model_name)
    for w in all_widget_types:
        name = w['name']
        parser: PydanticOutputParser = w['parser']
        parser_fixer = RetryOutputParser.from_llm(
            llm=chat_model, parser=parser, max_retries=10
        )
        prompt = ChatPromptTemplate.from_messages(
            widget_template,
        ).partial(
            format_instructions=parser_fixer.get_format_instructions(),
            widget_type=w['name'],
            widget_description=w['description'],
        )
        completion_chain = prompt | chat_model
        destination_chains[name] = partial(
            create_chain_function,
            completion_chain=completion_chain,
            prompt=prompt,
            parser=parser,
            parser_fixer=parser_fixer,
        )
    return destination_chains


def generate_router(
    container: Container, input_data: ParsedReportGeneratorInput
) -> Callable:
    chat_model = container.openai_supplier.get_model(input_data.model_name)

    destinations = [f"{w['name']}: {w['description']}" for w in all_widget_types]
    destinations_str = '\n'.join(destinations)

    parser = PydanticOutputParser(pydantic_object=LLMWidgetType)
    parser_fixer = RetryOutputParser.from_llm(
        llm=chat_model, parser=parser, max_retries=10
    )
    prompt = ChatPromptTemplate.from_messages(
        router_template,
    ).partial(
        widget_description_list=destinations_str,
        format_instructions=parser_fixer.get_format_instructions(),
    )
    completion_chain: LLMChain = prompt | chat_model
    router_chain_func = partial(
        create_chain_function,
        completion_chain=completion_chain,
        prompt=prompt,
        parser=parser,
        parser_fixer=parser_fixer,
    )
    return router_chain_func
