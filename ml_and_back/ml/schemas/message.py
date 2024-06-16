from .base import CamelizedBaseModel


class ChatResponseTemplateGenerator(CamelizedBaseModel):
    """Chat response schema."""

    message: str


class TemplateGeneratorInput(CamelizedBaseModel):
    """Input for template generator"""

    input_theme: str
    model_name: str
