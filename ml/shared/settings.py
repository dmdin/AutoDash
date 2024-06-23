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

    redis_host: str = 'redis'
    redis_port: int = 6379

    search_host: str = 'search'
    search_port: int = 8000

    chroma_host: str = 'chroma'
    chroma_port: int = 8000

    llm_data_path: str = 'data/'

    uvicorn_host: str = '0.0.0.0'
    uvicorn_port: int = 8000
    uvicorn_workers: int = mp.cpu_count()
    uvicorn_log_level: str = 'WARNING'

    class Config:
        env_file = '.env'
        env_prefix = '_'
        env_nested_delimiter = '__'


app_settings = AppSettings()
