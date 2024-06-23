import enum
import string

from llm.report.model import ReportTemplate
from supplier.openapi_supplier import OPENAI_MODELS

from .base import CamelizedBaseModel


class RawReportGeneratorInput(CamelizedBaseModel):
    """Input for template report"""

    report_theme: str
    report_text: str
    model_name: OPENAI_MODELS
    urls: list[str] | None


class ParsedReportGeneratorInput(CamelizedBaseModel):
    """Input for template report"""

    report_theme: str
    report_template: ReportTemplate
    model_name: OPENAI_MODELS
    urls: list[str] | None


class WidgetChartType(enum.StrEnum):
    PIE = 'pie'
    BAR = 'bar'
    LINE = 'line'
    TEXT = 'text'
    BADGE = 'badge'


class WidgetSource(CamelizedBaseModel):
    url: string
    text: string


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


AllWidgets = (
    BarChartWidget
    | TextChartWidget
    | LineChartWidget
    | PieChartWidget
    | BadgeChartWidget
)


class WidgetBlock(CamelizedBaseModel):
    block_name: str
    widgets: list[AllWidgets]


class ReportOutput(CamelizedBaseModel):
    blocks: list[WidgetBlock]
