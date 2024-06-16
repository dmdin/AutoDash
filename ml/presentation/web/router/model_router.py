from fastapi import APIRouter, WebSocket
import httpx
import ujson
from schemas.parser import ParserDocument, SourceDocuments
from schemas.widget import ReportOutput, Widget, TemplateReportInput
from presentation.dependencies import container
from schemas.message import TemplateGeneratorInput
from langchain.schema import BaseMessage
from langchain_community.vectorstores.redis import Redis
from langchain.docstore.document import Document
from shared.settings import app_settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

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


def parse_documents_from_search(documents: list[ParserDocument]) -> list[Document]:
    langchain_documents: list[Document] = []
    for doc in documents:
        new_doc = Document(
            doc['all_text_from_page'], page_title=doc['page_title'], url=doc['url']
        )
        langchain_documents.append(new_doc)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
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
    report_theme: str,
    urls: SourceDocuments,
    report_template: TemplateReportInput,
    model_name: str = 'gpt-4o',
) -> ReportOutput:
    all_documents_from_search_raw = await search_data_for_llm(
        query=report_theme, urls=urls
    )
    print(all_documents_from_search_raw)
    langchain_documents = parse_documents_from_search(all_documents_from_search_raw)
    rds = Redis.from_documents(
        langchain_documents,
        embedding=container.openai_supplier.embeddings,
        redis_url=f'redis://{app_settings.redis_host}:{app_settings.redis_port}',
    )
    index_name = rds.index_name
    retriever = rds.as_retriever(search_kwargs={'k': 12})
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
            'Хорошо, я внимательно изучил шаблон и буду стараться следовать ему, а именно правильно выбирать нужные виджеты !',
        ),
        (
            'user',
            'Подготовь, пожалуйста, для меня отчёт по выбранной теме: {report_theme}, для этого напшии мне JSON с правильной схемой, для этого ознакомься со структурой виджетов:\n{format_instructions}\nПожалуйста, верни только виджеты с отчётами! Сделай это на самом профессиональном уровне!',
        ),
    ])

    parser = JsonOutputParser(pydantic_object=list[Widget])
    model = container.openai_supplier.get_model(model_name)

    rag_chain = (
        {
            'context': retriever | format_docs,
            'report_theme': report_theme,
            'report_template': report_template,
            'format_instrucitons': parser.get_format_instructions(),
        }
        | prompt_template
        | model
        | parser
    )

    response = await rag_chain.invoke()
    response_content = ujson.loads(response.content)

    final_response = ReportOutput(redis_index_name=index_name, widgets=response_content)
    return final_response.json()
