import enum

from pydantic import Field

from .base import CamelizedBaseModel


class ChartTypes(enum.StrEnum):
    PIE = 'pie'
    BAR = 'bar'
    LINE = 'line'
    TEXT = 'text'
    TABLE = 'table'


class ChartData(CamelizedBaseModel):
    name: str = Field(
        description='название сущности, к которым принадлежит данная единица информации'
    )
    value: float = Field(description='значение данных')


class ChartSeries(CamelizedBaseModel):
    name: str = Field(description='название данных')
    unit: str = Field(description='единица измерения данных')
    data: list[ChartData] = Field(
        description='массив данных для отображения в виджете, все данные должны совпадать по тематике в выбранной группе'
    )


class Widget(CamelizedBaseModel):
    type: ChartTypes = Field(description='тип возвращаемого виджета')
    title: str = Field(description='название виджета')
    subtitle: str = Field(description='дополнительное пояснение по данным в виджете')
    category: list[str] = Field(
        description='необязательное поле, которое может содержать данные о том, как лучше разбивать данные, например, информацию по годам в формате [2022, 2023]'
    )
    series: list[ChartSeries] = Field(
        description='группа данных, объединённых одной тематикой, зачастую содержит только одну группу с пустым именем, так как каждый виджет зачастую описывает только одну группу данных'
    )


class LLMReportOutput(CamelizedBaseModel):
    widgets: list[Widget] = Field(
        description='список всех виджетов, используемых в отчёте'
    )


class ReportOutput(CamelizedBaseModel):
    redis_index_name: str
    widgets: list[Widget]
