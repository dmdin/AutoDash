from .base import CamelizedBaseModel


class ChatResponseTemplateGenerator(CamelizedBaseModel):
    """Chat response schema."""

    message: str
