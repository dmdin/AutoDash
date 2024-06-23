from llm.utils import create_widget_response, format_docs
from schemas.report_widget import (
    AllWidgets,
    ParsedReportGeneratorInput,
    WidgetBlock,
    WidgetSource,
)
from shared.containers import Container

from .model import LLMWidgetType
from .router import generate_destinations, generate_router


async def generate_report(
    container: Container,
    input_data: ParsedReportGeneratorInput,
):
    router_chain = generate_router(container, input_data)
    destination_chains = generate_destinations(container, input_data)

    for block in input_data.report_template.blocks:
        block_name = block.block_name
        block_widgets: list[AllWidgets] = []
        for point in block.points:
            llm_input = {
                'input_theme': input_data.report_theme,
                'block_name': block_name,
                'point_name': point,
            }
            route_response: LLMWidgetType = await router_chain.ainvoke(llm_input)
            widget_chain = destination_chains[str(route_response.chosen_widget_type)]

            search_query = f'Тема - {input_data.report_theme}, блок - {block_name}, пункт - {point}'
            all_documents_from_search_raw = (
                await container.search_supplier.search_data_for_llm(
                    query=search_query, urls=input_data.urls
                )
            )
            langchain_documents = container.search_supplier.parse_documents_from_search(
                all_documents_from_search_raw
            )
            if langchain_documents:
                container.retriever_service.retriever.add_documents(langchain_documents)

            retrieved_docs = await container.retriever_service.retriever.ainvoke(
                search_query
            )
            if retrieved_docs:
                sources = [
                    WidgetSource(url=x.metadata['url'], text=x.page_content)
                    for x in retrieved_docs
                ]
                context = format_docs(retrieved_docs)
            else:
                sources = [
                    WidgetSource(
                        url='chat.openai.com',
                        text='Information was gathered from External Knowledge Base (ChatGPT)',
                    )
                ]
                context = 'Никакой информации не получилось найти, поэтому используй информацию из ChatGPT'

            widget_response = await widget_chain.ainvoke({
                'input_theme': input_data.report_theme,
                'point_name': point,
                'block_name': block_name,
                'context': context,
            })

            final_widget_response = create_widget_response(
                widget_response, route_response, sources=sources
            )
            block_widgets.append(final_widget_response)

        widget_block_response = WidgetBlock(
            block_name=block_name, widgets=block_widgets
        )
        yield widget_block_response
