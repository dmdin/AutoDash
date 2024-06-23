from pydantic import Field

from schemas.base import CamelizedBaseModel
from schemas.report_widget import WidgetChartType


class LLMWidgetType(CamelizedBaseModel):
    chosen_widget_type: WidgetChartType = Field(description='выбранный тип виджета')
