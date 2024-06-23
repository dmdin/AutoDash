from .base import CamelizedBaseModel


class SearchParsedDocumentResult(CamelizedBaseModel):
    title: str
    text: str
    url: str
    extra_data: dict[str, str]
    html: str


class SearchParsedDocumentList(CamelizedBaseModel):
    """
    Формат документа, с указанным url страницы
    В all_text_from_page содержится все полученные со страницы текстовые данные
    В page_title хранится имя страницы (при наличии)
    """

    results: list[SearchParsedDocumentResult]
    errors: list[dict[str, str]]
