import enum

from schemas.base import CamelizedBaseModel


class HealthStatuses(enum.StrEnum):
    OK = 'OK'
    ERR = 'ERR'


class HealthResponse(CamelizedBaseModel):
    status: HealthStatuses
    error: str | None = None
