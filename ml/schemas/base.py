from typing import Any

from fastapi.encoders import jsonable_encoder as _jsonable_encoder
from pydantic import BaseModel


# * Pure pydantic model without any alias generator
class PureBaseModel(BaseModel):
    def jsonable_encoder(self, **kwargs: Any) -> Any:
        return _jsonable_encoder(self, **kwargs)

    class Config:
        populate_by_name = True
        from_attributes = True


# # * Camel alias generator model
class CamelizedBaseModel(PureBaseModel):
    pass
