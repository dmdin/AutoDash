import enum

from llm.report.model import ReportTemplate
from supplier.openapi_supplier import OPENAI_MODELS

from .base import CamelizedBaseModel


class RawReportGeneratorInput(CamelizedBaseModel):
    """Input for template report"""

    report_theme: str
    report_text: str
    model_name: OPENAI_MODELS = OPENAI_MODELS.GPT_3_5_TURBO
    urls: list[str] = []


class ParsedReportGeneratorInput(CamelizedBaseModel):
    """Input for template report"""

    report_theme: str
    report_template: ReportTemplate
    model_name: OPENAI_MODELS = OPENAI_MODELS.GPT_3_5_TURBO
    urls: list[str] = []


class WidgetChartType(enum.StrEnum):
    BADGE = 'badge'
    BAR = 'bar'
    LINE = 'line'
    PIE = 'pie'
    # TABLE = 'table'
    TEXT = 'text'
    NONE = 'none'


class WidgetSource(CamelizedBaseModel):
    url: str
    text: str


class AbstractWidget(CamelizedBaseModel):
    type: WidgetChartType
    title: str
    sources: list[WidgetSource]


class BarChartWidget(AbstractWidget):
    type: WidgetChartType = WidgetChartType.BAR
    categories: list[str]
    unit: str
    data: list[int | float]


class TextChartWidget(AbstractWidget):
    type: WidgetChartType = WidgetChartType.TEXT
    text: str


class LineChartWidget(AbstractWidget):
    type: WidgetChartType = WidgetChartType.LINE
    categories: list[str]
    unit: str
    data: list[int | float]


class PiePiece(CamelizedBaseModel):
    name: str
    value: int | float


class PieChartWidget(AbstractWidget):
    type: WidgetChartType = WidgetChartType.PIE
    unit: str
    data: list[PiePiece]


class BadgeChartWidget(AbstractWidget):
    type: WidgetChartType = WidgetChartType.BADGE
    data: int | float


class TableChartWidget(AbstractWidget):
    type: WidgetChartType = WidgetChartType.TABLE
    categories: list[str]
    rows: list[list[str | int | float]]


AllWidgets = (
    BarChartWidget
    | TextChartWidget
    | LineChartWidget
    | PieChartWidget
    | BadgeChartWidget
    | TableChartWidget
)


class WidgetBlock(CamelizedBaseModel):
    block_name: str
    widgets: list[AllWidgets]


class ReportOutput(CamelizedBaseModel):
    blocks: list[WidgetBlock]
