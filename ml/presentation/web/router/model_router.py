import ujson as json
from fastapi import APIRouter, WebSocket

from llm.report import agent as report_agent
from llm.report.model import ReportTemplate
from llm.widget import agent as widget_agent
from presentation.dependencies import container
from schemas.report_template import (
    ReportTemplateGeneratorInput,
    ReportTemplateParserInput,
)
from schemas.report_widget import (
    ParsedReportGeneratorInput,
    RawReportGeneratorInput,
    ReportOutput,
)
from shared.base import logger
from supplier.openapi_supplier import OPENAI_MODELS

router = APIRouter(prefix='/llm')


@router.get(
    '/generate_template',
    response_model=ReportTemplate,
    response_model_exclude_none=True,
)
async def generate_template(
    query: str, model_name: OPENAI_MODELS, use_template_w_examples: bool
) -> ReportTemplate:
    """
    Generate template
    """
    input_data = ReportTemplateGeneratorInput(
        input_theme=query,
        model_name=model_name,
        use_template_w_examples=use_template_w_examples,
    )
    all_blocks = []
    async for block in report_agent.generate_template(container, input_data):
        all_blocks.append(block)
    return ReportTemplate(blocks=all_blocks)


@router.websocket(
    '/generate_template',
)
async def generate_template_websocket(websocket: WebSocket) -> None:
    """
    Generate template
    """
    await websocket.accept()
    try:
        raw_data = await websocket.receive_json()
        input_data = ReportTemplateGeneratorInput(**raw_data)
        async for block in report_agent.generate_template(container, input_data):
            await websocket.send_json(block.dict())
        await websocket.send_text('finish')
        await websocket.close()
    except Exception as e:  # TODO: mb smth better
        logger.debug(f'Error occured: {e}')
        await websocket.close(
            code=1011,
            reason=json.dumps({
                'code': 500,
                'error': 'Error occured on server. Please contact administrator.',
            }),
        )


@router.post(
    '/create_base_report',
    response_model=ReportOutput,
    response_model_exclude_none=True,
)
async def create_report(
    report_input: RawReportGeneratorInput,
) -> ReportOutput:
    report_template_response = await report_agent.parse_template(
        container=container,
        input_data=ReportTemplateParserInput(
            input_theme=report_input.report_theme,
            raw_report_template_text=report_input.report_text,
            model_name=report_input.model_name,
        ),
    )
    input_data = ParsedReportGeneratorInput(
        report_theme=report_input.report_theme,
        report_template=report_template_response,
        model_name=report_input.model_name,
        urls=report_input.urls,
    )

    all_blocks = []
    async for block in widget_agent.generate_report(
        container=container, input_data=input_data
    ):
        all_blocks.append(block)
    final_response = ReportOutput(blocks=all_blocks)
    return final_response


@router.websocket('/create_base_report')
async def create_report_websocket(websocket: WebSocket) -> None:
    """
    Create report websocket
    """
    await websocket.accept()
    try:
        raw_data = await websocket.receive_json()
        raw_input_data = RawReportGeneratorInput(**raw_data)
        report_template_response = await report_agent.parse_template(
            container=container,
            input_data=ReportTemplateParserInput(
                input_theme=raw_input_data.report_theme,
                raw_report_template_text=raw_input_data.report_text,
                model_name=raw_input_data.model_name,
            ),
        )
        input_data = ParsedReportGeneratorInput(
            report_theme=raw_input_data.report_theme,
            report_template=report_template_response,
            model_name=raw_input_data.model_name,
            urls=raw_input_data.urls,
        )
        async for block in widget_agent.generate_report(
            container=container, input_data=input_data
        ):
            await websocket.send_json(block.dict())
        await websocket.send_text('finish')
        await websocket.close()
    except Exception as e:  # TODO: mb smth better
        logger.debug(f'Error occured: {e}')
        await websocket.close(
            code=1011,
            reason=json.dumps({
                'code': 500,
                'error': 'Error occured on server. Please contact administrator.',
            }),
        )
