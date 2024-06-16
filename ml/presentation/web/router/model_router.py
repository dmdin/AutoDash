from fastapi import APIRouter, WebSocket
import httpx
import uuid

from pydantic import ValidationError
from schemas.parser import ParserDocument, SourceDocuments
from schemas.widget import LLMReportOutput, ReportOutput, TemplateReportInput
from presentation.dependencies import container
from schemas.message import TemplateGeneratorInput
from langchain.schema import BaseMessage
from langchain_community.vectorstores.chroma import Chroma
from langchain.docstore.document import Document
from shared.settings import app_settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from shared.base import logger
from langchain_core.runnables import RunnablePassthrough

router = APIRouter(prefix='/llm')


async def search_data_for_llm(query: str, urls: SourceDocuments):
    api_url = f'http://{app_settings.parser_host}:{app_settings.parser_port}/search_data_for_llm'
    async with httpx.AsyncClient() as client:
        try:
            response: httpx.Response = await client.post(
                api_url, params={'query': query}, data=urls.json()
            )
            all_documents: list[ParserDocument] = response.json()
        except httpx.HTTPError:
            all_documents: list[ParserDocument] = []
        return all_documents


@router.websocket(
    '/generate_template',
)
async def generate_template(websocket: WebSocket) -> str:
    """
    Returns all documents suitable for RAG
    """
    await websocket.accept()
    try:
        raw_data = await websocket.receive_json()
        data = TemplateGeneratorInput(
            input_theme=raw_data['input_theme'], model_name=raw_data['model_name']
        )
        template: BaseMessage
        async for template in container.openai_supplier.generate_template(
            data.input_theme, data.model_name
        ):
            response = template.content
            await websocket.send_text(response)
    except Exception as e: # TODO: mb smth better
        logger.debug(f"!!!!!!!!!!!!!!!!!! {e}")



def parse_documents_from_search(documents: list[ParserDocument]) -> list[Document]:
    langchain_documents: list[Document] = []
    for doc in documents:
        try:
            new_doc = Document(
                doc['all_text_from_page'], page_title=doc['page_title'], url=doc['url']
            )
            langchain_documents.append(new_doc)
        except Exception as e:
            logger.debug(e)
            continue
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=256)
    splitted_langchain_documents = text_splitter.split_documents(langchain_documents)
    return splitted_langchain_documents


def format_docs(docs: list[Document]):
    return '\n\n'.join(doc.page_content for doc in docs)


@router.post(
    '/create_report',
    response_model=ReportOutput,
    response_model_exclude_none=True,
)
async def create_report(
    urls: SourceDocuments,
    report_item: TemplateReportInput,
    model_name: str = 'gpt-4o',
) -> ReportOutput:
    all_documents_from_search_raw = await search_data_for_llm(
        query=report_item.report_theme, urls=urls
    )
    logger.debug(f'Info: {all_documents_from_search_raw}')
    langchain_documents = parse_documents_from_search(all_documents_from_search_raw)
    collection_index_name = uuid.uuid4().hex
    cds = Chroma.from_documents(
        langchain_documents,
        embedding=container.openai_supplier.embeddings,
        collection_name=collection_index_name,
    )
    retriever = cds.as_retriever(search_kwargs={'k': 8})
    prompt_template = ChatPromptTemplate.from_messages([
        (
            'system',
            'Ты - умный помощник в составлении шаблонов отчётов по выбранной тематике, ты умеешь правильно делать JSON выводы по заданной структуре.',
        ),
        (
            'user',
            'Изучи данный шаблон и проанализируй каждый блок, указанные в шаблоне для создания релевантных виджетов для отчёта относительно плана, предоставленного в шаблоне. Тема: {report_theme}, сам текст шаблона: {report_template}.',
        ),
        (
            'ai',
            'Хорошо, я внимательно изучил шаблон и буду стараться следовать ему, а именно правильно выбирать нужные виджеты!',
        ),
        (
            'user',
            'Подготовь, пожалуйста, для меня отчёт по выбранной теме: {report_theme}. Используй информацию отсюда:\n{context}\n. Для создания отчёта напшии мне JSON с правильной схемой, для этого ознакомься со структурой виджетов:\n{format_instructions}\nПожалуйста, верни только виджеты! Сделай это на самом профессиональном уровне!',
        ),
    ])

    parser = JsonOutputParser(pydantic_object=LLMReportOutput)
    model = container.openai_supplier.get_model(model_name)

    retrieved_documents = await retriever.ainvoke(
        f'Тема: {report_item.report_theme}, части отчёта: {report_item.report_text}'
    )
    retrieved_documents_string = format_docs(retrieved_documents)

    rag_chain = RunnablePassthrough() | prompt_template | model | parser

    while True:
        try:
            response = await rag_chain.ainvoke({
                'report_theme': report_item,
                'report_template': report_item.report_text,
                'context': retrieved_documents_string,
                'format_instructions': parser.get_format_instructions(),
            })

            print(response)

            final_response = ReportOutput(
                collection_index_name=collection_index_name, widgets=response['widgets']
            )
            print(final_response)
            return final_response
        except ValidationError as e:
            logger.debug(e)
            continue
        except Exception as e:
            logger.debug('UNKOWN!')
            logger.debug(e)
            continue
