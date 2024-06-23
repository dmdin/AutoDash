from supplier.openapi_supplier import OPENAI_MODELS

from .base import CamelizedBaseModel


class ReportTemplateGeneratorInput(CamelizedBaseModel):
    """Input for report template generator"""

    input_theme: str
    model_name: OPENAI_MODELS
    use_template_w_examples: bool = False
    n_blocks: int = -1


class ReportTemplateParserInput(CamelizedBaseModel):
    """Input for report template parser"""

    input_theme: str
    raw_report_template_text: str
    model_name: OPENAI_MODELS
