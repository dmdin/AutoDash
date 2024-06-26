from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import urllib.parse
import requests
import aiohttp
import asyncio
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import random
import ssl

load_dotenv()
app = FastAPI()


class URLItem(BaseModel):
    url: str
    return_html: Optional[bool] = False
    extra_data: Optional[bool] = False


class URLListItem(BaseModel):
    urls: List[str]
    return_html: Optional[bool] = False
    extra_data: Optional[bool] = False


class URLListItemSearch(URLListItem):
    query: str
    links_number: Optional[int] = 10
    to_page: Optional[int] = 0


class Article(BaseModel):
    title: str
    text: str
    url: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    html: Optional[str] = None


class SearchResult(BaseModel):
    results: List[Article]
    errors: List[Dict[str, str]]


def clean_title(title: str) -> str:
    return ' '.join(title.split()).replace('\n', ' ').replace('|', '-').strip()


def parse_yandex_xml(xml_data: str) -> List[Dict[str, str]]:
    root = ET.fromstring(xml_data)
    results = []
    for group in root.findall('.//group'):
        doc = group.find('doc')
        if doc is not None:
            url = doc.find('url').text if doc.find('url') is not None else ""
            title_element = doc.find('title')
            title = ''.join(title_element.itertext()).strip() if title_element is not None else ""
            cleaned_title = clean_title(title)
            results.append({"url": url, "title": cleaned_title})
    return results


async def fetch_html(url: str, timeout: int = 3) -> str:
    REQUEST_HEADERS = {
        'User-Agent': random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        ]),
    }
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=REQUEST_HEADERS, ssl=ssl_context, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                text = await response.text()
                if response.status != 200 or (len(text) < 200 and "captcha" in text.lower()):
                    raise HTTPException(status_code=response.status, detail="Доступ к контенту ограничен или требуется капча")
                return text
        except asyncio.TimeoutError:
            raise HTTPException(status_code=408, detail="Request Timeout")


def extract_comnews_body(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for ad_block in soup.find_all('script'):
        ad_block.decompose()
    for ad_block in soup.find_all('blockquote', {'class': 'quote4'}):
        ad_block.decompose()
    main_content = soup.find('div', {'class': 'field field-text full-html field-name-body'})
    return main_content.get_text(separator='\n').strip() if main_content else None


def parse_rbc_article(html_content: str, return_html: bool, extra_data: bool) -> Optional[Dict[str, Any]]:
    soup = BeautifulSoup(html_content, 'html.parser')
    article = soup.find('article', class_='article-feature-item')
    if not article:
        return None
    title_tag = article.find('h1', class_='article-entry-title')
    title = title_tag.get_text(strip=True) if title_tag else "Заголовок не найден"
    paragraphs = article.find_all('p', class_='paragraph')
    text = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
    article_dict = {"title": title, "text": text}
    if extra_data:
        article_dict["extra_data"] = {
            "num_paragraphs": len(paragraphs),
            "first_paragraph": paragraphs[0].get_text(strip=True) if paragraphs else ""
        }
    if return_html:
        article_dict["html"] = html_content
    return article_dict


def parse_kommersant_article(html_content: str, return_html: bool, extra_data: bool) -> Optional[Dict[str, Any]]:
    soup = BeautifulSoup(html_content, 'html.parser')
    first_article = soup.find('article') or soup.find('div', class_='article-class') or soup.find('section',
                                                                                                  class_='article-class')
    if first_article:
        title_tag = first_article.find(['h1', 'h2', 'h3'])
        title = title_tag.get_text(strip=True) if title_tag else "Заголовок не найден"
        paragraphs = first_article.find_all('p')
        text = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
        article_dict = {"title": title, "text": text}
        if extra_data:
            article_dict["extra_data"] = {
                "num_paragraphs": len(paragraphs),
                "first_paragraph": paragraphs[0].get_text(strip=True) if paragraphs else ""
            }
        if return_html:
            article_dict["html"] = html_content
        return article_dict
    else:
        return None


def parse_tadviser_article(html_content: str, return_html: bool, extra_data: bool) -> Optional[Dict[str, Any]]:
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', {'class': 'pub_body'})
    if main_content:
        paragraphs = main_content.find_all('p')
        text = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
        title_tag = soup.find(['h1', 'h2', 'h3'])
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        article_dict = {"text": text, "title": title}
        if extra_data:
            article_dict["extra_data"] = {
                "num_paragraphs": len(paragraphs),
                "first_paragraph": paragraphs[0].get_text(strip=True) if paragraphs else ""
            }
        if return_html:
            article_dict["html"] = html_content
        return article_dict
    else:
        return None


def parse_cnews_article(html_content: str, return_html: bool, extra_data: bool) -> Optional[Dict[str, Any]]:
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('article', class_='news_container')
    if main_content:
        paragraphs = main_content.find_all('p')
        text = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
        title_tag = soup.find(['h1', 'h2', 'h3'])
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        article_dict = {"text": text, "title": title}
        if extra_data:
            article_dict["extra_data"] = {
                "num_paragraphs": len(paragraphs),
                "first_paragraph": paragraphs[0].get_text(strip=True) if paragraphs else ""
            }
        if return_html:
            article_dict["html"] = html_content
        return article_dict
    else:
        return None


async def get_page_content(url):
    try:
        REQUEST_HEADERS = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=REQUEST_HEADERS) as response:
                try:
                    response.raise_for_status()
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')

                    # Extract all text
                    texts = soup.stripped_strings
                    all_text = ' '.join(texts)

                    # Extract title
                    title = soup.title.string if soup.title else 'No title found'

                    return {
                        "url": url,
                        "all_text_from_page": all_text,
                        "page_title": title
                    }
                except Exception as e:
                    return {
                        "url": url,
                        "all_text_from_page": "",
                        "page_title": 'No title found'
                    }
    except aiohttp.ClientError as e:
        return {
            "url": url,
            "error": str(e)
        }


async def parse_article(html_content: str, domain: str, return_html: bool, extra_data: bool) -> Optional[
    Dict[str, Any]]:
    if "comnews" in domain:
        content = extract_comnews_body(html_content)
        if content:
            return {"title": "comnews article", "text": content, "extra_data": {},
                    "html": html_content if return_html else None}
    elif "rbc" in domain:
        return parse_rbc_article(html_content, return_html, extra_data)
    elif "kommersant" in domain:
        return parse_kommersant_article(html_content, return_html, extra_data)
    elif "tadviser" in domain:
        return parse_tadviser_article(html_content, return_html, extra_data)
    elif "cnews" in domain:
        return parse_cnews_article(html_content, return_html, extra_data)
    else:
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find(['h1', 'h2', 'h3'])
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        paragraphs = soup.find_all('p')
        text = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
        article_dict = {"title": title, "text": text}
        if extra_data:
            article_dict["extra_data"] = {
                "num_paragraphs": len(paragraphs),
                "first_paragraph": paragraphs[0].get_text(strip=True) if paragraphs else ""
            }
        if return_html:
            article_dict["html"] = html_content
        article_dict["url"] = domain
        return article_dict


def search_func(query: str, sources: List[str], to_page: int = 0) -> List[Dict[str, str]]:
    try:
        encoded_query = urllib.parse.quote(query)
        if sources:
            encoded_query = "%20|%20".join([f"site:{url}%20{encoded_query}" for url in sources])
        parsed = []
        for page in range(to_page + 1):
            yandex_url = f"https://yandex.ru/search/xml?folderid={os.getenv('yandex_folderid')}&apikey={os.getenv('yandex_apikey')}&query={encoded_query}&page={page}"
            response = requests.get(yandex_url)
            xml_data = response.text
            parsed_data = parse_yandex_xml(xml_data)
            parsed.extend(parsed_data)
        # print(f"{parsed = }")
        return parsed
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
async def ping():
    return 'pong'

@app.post("/search")
async def search(query: str, sources: Optional[URLListItem] = None):
    return search_func(query, sources.urls if sources else [])


@app.post("/extract", response_model=List[dict])
async def extract(url_list: URLListItem):
    if not isinstance(url_list.urls, list):
        raise HTTPException(status_code=400, detail="URLs should be provided as a list")

    tasks = [get_page_content(url) for url in url_list.urls]
    results = await asyncio.gather(*tasks)
    return results


@app.post("/parse", response_model=Article)
async def parse_url(item: URLItem):
    try:
        html_content = await fetch_html(item.url)
        domain = item.url
        parsed_article = await parse_article(html_content, domain, item.return_html, item.extra_data)
        if parsed_article is None or len(parsed_article.get("text").rstrip()) == 0:
            raise HTTPException(status_code=404, detail="Статья не найдена")
        return parsed_article
    except HTTPException as e:
        return {"url": item.url, "error": str(e.detail)}

@app.post("/parse_multiple", response_model=SearchResult)

async def parse_urls(item: URLListItem):
    semaphore = asyncio.Semaphore(20)  # Ограничение на количество одновременных запросов

    async def fetch_and_parse(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        async with semaphore:
            try:
                html_content = await fetch_html(url)
                parsed_article = await parse_article(html_content, url, item.return_html, item.extra_data)
                if parsed_article is None or len(parsed_article.get("text", "").strip()) < 100:
                    return {"url": url, "error": "Статья не найдена"}
                parsed_article["url"] = url
                return parsed_article
            except Exception as e:
                return {"url": url, "error": str(e)}

    batch_size = 50  # Увеличение размера батча для улучшения производительности
    results = []
    errors = []

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(item.urls), batch_size):
            batch_urls = item.urls[i:i + batch_size]
            tasks = [fetch_and_parse(session, url) for url in batch_urls]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in batch_results:
                if isinstance(result, dict) and "error" in result:
                    errors.append(result)
                elif isinstance(result, dict):
                    results.append(result)

    # print(f"!!!!!!!!!!!!! results_len = {len(errors) + len(results)}")

    return {"results": results, "errors": errors}

@app.post("/search_data_for_llm")
async def search_data_for_llm(query: str, sources: Optional[URLListItem] = None):
    try:
        # Step 1: Perform the search
        parsed_data = search_func(query, sources.urls if sources else [])

        # Step 2: Extract content from the search results
        url_list = [item['url'] for item in parsed_data]
        tasks = [get_page_content(url) for url in url_list]
        extract_results = await asyncio.gather(*tasks)

        return extract_results
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search_data_for_llm_v2", response_model=SearchResult)
async def search_data_for_llm_v2(item: URLListItemSearch):
    try:
        if item.links_number:
            item.to_page = (item.links_number // 10) + int(item.links_number % 10 == 0)
        parsed_data = search_func(item.query, item.urls, item.to_page)
        url_list = [entry['url'] for entry in parsed_data]
        url_list_item = URLListItem(query=item.query, urls=url_list, return_html=item.return_html,
                                    extra_data=item.extra_data, to_page=item.to_page)
        parse_results = await parse_urls(url_list_item)
        # print(f"{item.urls = } with result = {parse_results['results'] = }; {parse_results['errors'] = }")
        if len(parse_results['results']) == 0:
            raise HTTPException(status_code=404, detail="No results found")
        return parse_results
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
