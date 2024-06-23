from langchain.chains.llm import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate

from schemas.report_widget import ParsedReportGeneratorInput, WidgetChartType
from shared.containers import Container

from .model import LLMWidgetType
from .templates import router_template, widget_template
from .widget_type import all_widget_types


def generate_destinations(
    container: Container, input_data: ParsedReportGeneratorInput
) -> dict[WidgetChartType, LLMChain]:
    destination_chains: dict[WidgetChartType, LLMChain] = {}
    chat_model = container.openai_supplier.get_model(input_data.model_name)
    for w in all_widget_types:
        name = LLMWidgetType(chosen_widget_type=WidgetChartType(w['name']))
        parser: PydanticOutputParser = w['parser']
        prompt = ChatPromptTemplate.from_template(
            widget_template,
            partial_variables={'format_instructions': parser.get_format_instructions()},
        )
        chain: LLMChain = prompt | chat_model | parser
        destination_chains[name] = chain
    return destination_chains


def generate_router(
    container: Container, input_data: ParsedReportGeneratorInput
) -> LLMChain:
    chat_model = container.openai_supplier.get_model(input_data.model_name)

    destinations = [f"{w['name']}: {w['description']}" for w in all_widget_types]
    destinations_str = '\n'.join(destinations)

    parser = PydanticOutputParser(LLMWidgetType)
    prompt = ChatPromptTemplate.from_template(
        router_template,
        partial_variables={
            'widget_description_list': destinations_str,
            'format_instructions': parser.get_format_instructions(),
        },
    )
    router_chain: LLMChain = prompt | chat_model | parser
    return router_chain
