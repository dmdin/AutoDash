import multiprocessing as mp
from typing import Optional
from langchain.pydantic_v1 import BaseSettings


class AppSettings(BaseSettings):
    gigachat_api_key: Optional[str]
    gigachat_api_url: Optional[str]

    openai_api_key: Optional[str]
    openai_api_url: Optional[str]

    anthropic_api_key: Optional[str]
    anthropic_api_url: Optional[str]

    parser_host: str
    parser_port: int = 8000

    redis_host: str = 'localhost'
    redis_port: int = 6379

    uvicorn_host: str = 'localhost'
    uvicorn_port: int = 7000
    # uvicorn_workers: int = mp.cpu_count()
    uvicorn_workers: int = 1
    uvicorn_log_level: str = 'WARNING'

    class Config:
        env_file = '.env'
        env_prefix = '_'
        env_nested_delimiter = '__'


app_settings = AppSettings()
