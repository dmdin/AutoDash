from pydantic import BaseModel
from typing import Any, Dict
import json

class YandexConfig(BaseModel):
    folderid: str
    apikey: str

class Config(BaseModel):
    yandex: YandexConfig

def load_config(config_path: str = "config.json") -> Config:
    with open(config_path, "r") as f:
        config_data: Dict[str, Any] = json.load(f)
    return Config(**config_data)

config = load_config()
