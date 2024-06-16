from .base import CamelizedBaseModel


class ParserDocument(CamelizedBaseModel):
    '''
    ```
    Формат документа, с указанным url страницы
    В all_text_from_page содержится все полученные со страницы текстовые данные
    В page_title хранится имя страницы (при наличии)
    ```
    '''
    url: str
    all_text_from_page: str
    page_title: str


class SourceDocuments(CamelizedBaseModel):
    '''
    ```
    Описание источников для поиска
    urls содержит список нужных url-ов
    ```
    '''
    urls: list[str] = []
