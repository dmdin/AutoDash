from dataclasses import dataclass
from enum import Enum

import ujson as json
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from shared.settings import app_settings


class OPENAI_MODELS(str, Enum):
    GPT_4O = 'gpt-4o'
    GPT_4_TURBO = 'gpt-4-turbo'
    GPT_4 = 'gpt-4'
    GPT_3_5_TURBO = 'gpt-3.5-turbo'


@dataclass
class OpenAISupplier:
    def __post_init__(self):
        assert app_settings.openai_api_key
        self.embeddings: OpenAIEmbeddings = OpenAIEmbeddings(
            base_url=app_settings.openai_api_url,
            api_key=app_settings.openai_api_key,
            model='text-embedding-3-large',
        )
        self._block_examples = json.load(
            open(app_settings.llm_data_path + 'llm_block_examples.json', 'r')
        )
        self._few_shot_examples = json.load(
            open(app_settings.llm_data_path + 'llm_few_shot_examples.json', 'r')
        )

    def get_model(
        self, model_name: OPENAI_MODELS = OPENAI_MODELS.GPT_4O, streaming: bool = False
    ) -> ChatOpenAI:
        assert app_settings.openai_api_key
        chat: ChatOpenAI = ChatOpenAI(
            base_url=app_settings.openai_api_url,
            api_key=app_settings.openai_api_key,
            temperature=0.675,
            model=model_name,
            streaming=streaming,
        )
        return chat

    @property
    def few_shot_examples(self):
        return self._few_shot_examples

    @property
    def block_examples(self):
        return self._block_examples
