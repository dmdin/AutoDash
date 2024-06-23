from .badge_chart import LLMBadgeWidget, badge_widget_info
from .bar_chart import LLMBarWidget, bar_widget_info
from .line_chart import LLMLineWidget, line_widget_info
from .pie_chart import LLMPieWidget, pie_widget_info
from .table_chart import LLMTableWidget, table_widget_info
from .text_chart import LLMTextWidget, text_widget_info

all_widget_types = [
    badge_widget_info,
    bar_widget_info,
    line_widget_info,
    pie_widget_info,
    table_widget_info,
    text_widget_info,
]

widget_mapper = {
    'badge': LLMBadgeWidget,
    'bar': LLMBarWidget,
    'line': LLMLineWidget,
    'pie': LLMPieWidget,
    'table': LLMTableWidget,
    'text': LLMTextWidget,
}

__all__ = ['all_widget_types', 'widget_mapper']
