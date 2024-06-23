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

router = APIRouter(prefix='/llm')


@router.websocket(
    '/generate_template',
)
async def generate_template(websocket: WebSocket) -> None:
    """
    Generate template
    """
    await websocket.accept()
    try:
        raw_data = await websocket.receive_json()
        input_data = ReportTemplateGeneratorInput(**raw_data)
        async for block in report_agent.generate_template(container, input_data):
            await websocket.send_json(block)
    except Exception as e:  # TODO: mb smth better
        logger.debug(e)


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
    report_template = ReportTemplate(**report_template_response['response'])
    input_data = ParsedReportGeneratorInput(
        report_theme=report_input.report_theme,
        report_template=report_template,
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
        report_template = ReportTemplate(**report_template_response['response'])
        input_data = ParsedReportGeneratorInput(
            report_theme=raw_input_data.report_theme,
            report_template=report_template,
            model_name=raw_input_data.model_name,
            urls=raw_input_data.urls,
        )
        async for block in widget_agent.generate_report(
            container=container, input_data=input_data
        ):
            await websocket.send_json(block)
    except Exception as e:  # TODO: mb smth better
        logger.debug(e)
