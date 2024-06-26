import asyncio
import uuid
from time import time

from openai import RateLimitError

from llm.utils import create_widget_response, format_docs
from schemas.report_widget import (
    AllWidgets,
    ParsedReportGeneratorInput,
    WidgetBlock,
    WidgetChartType,
    WidgetSource,
)
from shared.base import logger
from shared.containers import Container

from .model import LLMWidgetType
from .router import generate_destinations, generate_router


async def populate_documents(
    container: Container, search_query: str, input_data: ParsedReportGeneratorInput
):
    all_documents_from_search_raw = await container.search_supplier.search_data_for_llm(
        query=search_query, urls=input_data.urls
    )
    logger.debug('Starting parsing documents from search')
    langchain_documents = container.search_supplier.parse_documents_from_search(
        all_documents_from_search_raw
    )
    logger.debug('Finished parsing documents from search')
    if langchain_documents:
        logger.debug(f'Starting adding documents {len(langchain_documents)}')
        for document in langchain_documents:
            container.retriever_service.retriever.add_documents([document])
        logger.debug(f'Finished adding documents {len(langchain_documents)}')


async def generate_report(
    container: Container,
    input_data: ParsedReportGeneratorInput,
):
    logging_time_start = time()
    router_chain_callable = generate_router(container, input_data)
    destination_chains = generate_destinations(container, input_data)

    collection_name = uuid.uuid4().hex
    vectorstore = container.chroma_repository.get_langchain_with_context(
        collection_name
    )
    container.retriever_service.recreate_retriever_with_context(vectorstore)

    for block in input_data.report_template.blocks:
        logging_block_time_start = time()
        block_name = block.block_name
        block_widgets: list[AllWidgets] = []
        for point in block.points:
            logging_block_point_time_start = time()
            search_query = f'Тема - {input_data.report_theme}, блок - {block_name}, пункт - {point}'
            context = 'пусто'
            sources = []

            await populate_documents(container, search_query, input_data)
            logger.debug(f'Starting retriever for {search_query}')
            retrieved_docs = await container.retriever_service.retriever.ainvoke(
                search_query
            )
            logger.debug(
                f'Finished retriever for {search_query} with {len(retrieved_docs)}'
            )
            if retrieved_docs:
                sources = [
                    WidgetSource(url=x.metadata['url'], text='') for x in retrieved_docs
                ]
                context = format_docs(retrieved_docs)
            else:
                await populate_documents(container, search_query, input_data)
                logger.debug(f'Starting retriever second time for {search_query}')
                retrieved_docs = await container.retriever_service.retriever.ainvoke(
                    search_query
                )
                logger.debug(
                    f'Finished retriever second time for {search_query} with {len(retrieved_docs)}'
                )
                if retrieved_docs:
                    sources = [
                        WidgetSource(url=x.metadata['url'], text=x.page_content)
                        for x in retrieved_docs
                    ]
                    context = format_docs(retrieved_docs)

            llm_input = {
                'input_theme': input_data.report_theme,
                'block_name': block_name,
                'point_name': point,
                'context': context,
            }
            route_response: LLMWidgetType = await router_chain_callable(
                input_kwargs=llm_input
            )
            if route_response.chosen_widget_type != WidgetChartType.NONE:
                widget_chain = destination_chains[
                    str(route_response.chosen_widget_type)
                ]
                widget_response = await widget_chain(input_kwargs=llm_input)
                if widget_response is not None:
                    try:
                        final_widget_response = create_widget_response(
                            widget_response, route_response, sources=sources
                        )
                    except RateLimitError:
                        await asyncio.sleep(60)
                        final_widget_response = create_widget_response(
                            widget_response, route_response, sources=sources
                        )
                    block_widgets.append(final_widget_response)
            else:
                logger.debug(f'Nothing was made for {search_query}')

            logger.debug(
                f"Time for the block's point report generation: {time() - logging_block_point_time_start}"
            )
            await asyncio.sleep(60)
        widget_block_response = WidgetBlock(
            block_name=block_name, widgets=block_widgets
        )
        yield widget_block_response
        logger.debug(
            f'Time for the block report generation: {time() - logging_block_time_start}'
        )
    logger.debug(f'Time for the full report generation: {time() - logging_time_start}')
