from .base import CamelizedBaseModel


class SearchParsedDocumentResult(CamelizedBaseModel):
    title: str | None
    text: str | None
    url: str | None
    extra_data: dict[str, str] | None
    html: str | None


class SearchParsedDocumentList(CamelizedBaseModel):
    """
    Формат документа, с указанным url страницы
    В all_text_from_page содержится все полученные со страницы текстовые данные
    В page_title хранится имя страницы (при наличии)
    """

    results: list[SearchParsedDocumentResult] | None
    errors: list[dict[str, str]] | None
