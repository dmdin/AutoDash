from langchain.docstore.document import Document

from schemas.report_widget import (
    AllWidgets,
    BadgeChartWidget,
    BarChartWidget,
    LineChartWidget,
    PieChartWidget,
    PiePiece,
    TableChartWidget,
    TextChartWidget,
    WidgetChartType,
    WidgetSource,
)

from .widget.model import LLMWidgetType


def format_docs(docs: list[Document]):
    return '\n\n'.join(doc.page_content for doc in docs)


def create_widget_response(
    llm_response: AllWidgets,
    llm_widget_type: LLMWidgetType,
    sources: list[WidgetSource],
):
    if llm_widget_type.chosen_widget_type == WidgetChartType.BADGE:
        return BadgeChartWidget(
            title=llm_response.title, data=llm_response.data, sources=sources
        )
    elif llm_widget_type.chosen_widget_type == WidgetChartType.BAR:
        return BarChartWidget(
            title=llm_response.title,
            categories=llm_response.categories,
            unit=llm_response.unit,
            data=llm_response.data,
            sources=sources,
        )
    elif llm_widget_type.chosen_widget_type == WidgetChartType.LINE:
        return LineChartWidget(
            title=llm_response.title,
            sources=sources,
            categories=llm_response.categories,
            unit=llm_response.unit,
            data=llm_response.data,
        )
    elif llm_widget_type.chosen_widget_type == WidgetChartType.PIE:
        return PieChartWidget(
            title=llm_response.title,
            sources=sources,
            unit=llm_response.unit,
            data=[PiePiece(name=x.name, value=x.value) for x in llm_response.data],
        )
    elif llm_widget_type.chosen_widget_type == WidgetChartType.TEXT:
        return TextChartWidget(
            title=llm_response.title, sources=sources, text=llm_response.text
        )
    elif llm_widget_type.chosen_widget_type == WidgetChartType.TABLE:
        return TableChartWidget(
            title='table',
            sources=sources,
            rows=llm_response.rows,
        )
    else:
        raise NotImplementedError
