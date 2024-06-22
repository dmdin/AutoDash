from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import urllib.parse
import requests
import aiohttp
import httpx
import random
import ssl
import asyncio
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

load_dotenv()
app = FastAPI()


class UrlList(BaseModel):
    urls: List[str]


def clean_title(title):
    return ' '.join(title.split()).replace('\n', ' ').replace('|', '-').strip()


def parse_yandex_xml(xml_data):
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


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # TODO: make dynamic
]


class URLItem(BaseModel):
    url: str
    return_html: Optional[bool] = False
    extra_data: Optional[bool] = False


class URLListItem(BaseModel):
    urls: List[str]
    return_html: Optional[bool] = False
    extra_data: Optional[bool] = False


async def fetch_html(client: httpx.AsyncClient, url: str) -> str:
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    response = await client.get(url, headers=headers, follow_redirects=True)

    if response.status_code != 200 or "captcha" in response.text.lower():
        raise HTTPException(status_code=response.status_code,
                            detail="Доступ к контенту ограничен или требуется капча")

    return response.text


def extract_comnews_body(html):
    soup = BeautifulSoup(html, 'html.parser')
    for ad_block in soup.find_all('script'):
        ad_block.decompose()
    for ad_block in soup.find_all('blockquote', {'class': 'quote4'}):
        ad_block.decompose()
    main_content = soup.find('div', {'class': 'field field-text full-html field-name-body'})
    return main_content.get_text(separator='\n').strip() if main_content else None


def parse_rbc_article(html_content: str, return_html: bool, extra_data: bool) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, 'html.parser')
    article = soup.find('article', class_='article-feature-item')
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
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


def parse_kommersant_article(html_content: str, return_html: bool, extra_data: bool) -> Dict[str, Any]:
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
        raise HTTPException(status_code=404, detail="Первый блок статьи не найден")


def parse_tadviser_article(html_content: str, return_html: bool, extra_data: bool) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', {'class': 'pub_body'})
    if main_content:
        paragraphs = main_content.find_all('p')
        text = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
        article_dict = {"text": text}
        if extra_data:
            article_dict["extra_data"] = {
                "num_paragraphs": len(paragraphs),
                "first_paragraph": paragraphs[0].get_text(strip=True) if paragraphs else ""
            }
        if return_html:
            article_dict["html"] = html_content
        return article_dict
    else:
        raise HTTPException(status_code=404, detail="Контент не найден")


def parse_cnews_article(html_content: str, return_html: bool, extra_data: bool) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('article', class_='news_container')
    if main_content:
        paragraphs = main_content.find_all('p')
        text = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
        article_dict = {"text": text}
        if extra_data:
            article_dict["extra_data"] = {
                "num_paragraphs": len(paragraphs),
                "first_paragraph": paragraphs[0].get_text(strip=True) if paragraphs else ""
            }
        if return_html:
            article_dict["html"] = html_content
        return article_dict
    else:
        raise HTTPException(status_code=404, detail="Контент не найден")


async def get_page_content(url):
    try:
        REQUEST_HEADERS = {
            'User-Agent': random.choice(user_agents),
        }
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=REQUEST_HEADERS, ssl=ssl_context) as response:
                try:
                    response.raise_for_status()
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    texts = soup.stripped_strings
                    all_text = ' '.join(texts)
                    title = soup.title.string if soup.title else 'No title found'
                    if title == 'No title found' and len(all_text.rstrip()) == 0:
                        raise HTTPException(status_code=404, detail="Контент не найден")
                    return {
                        "url": url,
                        "all_text_from_page": all_text,
                        "page_title": title
                    }
                except Exception as e:
                    return {
                        "url": url,
                        "error": str(e)
                    }
    except aiohttp.ClientError as e:
        return {
            "url": url,
            "error": str(e)
        }


async def parse_article(html_content: str, domain: str, return_html: bool, extra_data: bool) -> Dict[str, Any]:
    if "comnews" in domain:
        return {"content": extract_comnews_body(html_content)}
    elif "rbc" in domain:
        return parse_rbc_article(html_content, return_html, extra_data)
    elif "kommersant" in domain:
        return parse_kommersant_article(html_content, return_html, extra_data)
    elif "tadviser" in domain:
        return parse_tadviser_article(html_content, return_html, extra_data)
    elif "cnews" in domain:
        return parse_cnews_article(html_content, return_html, extra_data)
    else:
        return await get_page_content(domain)


def search_func(query: str, sources: List[str]):
    try:
        encoded_query = urllib.parse.quote(query)
        if sources and sources:
            encoded_query = ["site:" + urllib.parse.quote(url) + f"%20{encoded_query}" for url in sources]
            encoded_query = "%20|%20".join(encoded_query)

        yandex_url = f"https://yandex.ru/search/xml?folderid={os.getenv('yandex_folderid')}&apikey={os.getenv('yandex_apikey')}&query={encoded_query}"
        response = requests.get(yandex_url)
        xml_data = response.text
        parsed_data = parse_yandex_xml(xml_data)
        return parsed_data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search(query: str, sources: Optional[UrlList]):
    """
    You can choose which sources to use by changing body params
    {
      "urls": [
        "ru.wikipedia.org"
      ]
    }
     """
    return search_func(query, sources.urls)


@app.post("/extract", response_model=List[dict])
async def extract(url_list: UrlList):
    """
    Pass the urls for text extracting
    {
      "urls": [
        "ru.wikipedia.org"
      ]
    }
    """
    if not isinstance(url_list.urls, list):
        raise HTTPException(status_code=400, detail="URLs should be provided as a list")

    tasks = [get_page_content(url) for url in url_list.urls]
    results = await asyncio.gather(*tasks)
    return results


@app.post("/search_data_for_llm")
async def search_data_for_llm(query: str, sources: Optional[UrlList]):
    """
    You can choose which sources to use by changing body params
    {
      "urls": [
        "ru.wikipedia.org"
      ]
    }
    """
    try:
        # Step 1: Perform the search
        parsed_data = search_func(query, sources.urls)

        # Step 2: Extract content from the search results
        url_list = [item['url'] for item in parsed_data]
        tasks = [get_page_content(url) for url in url_list]
        extract_results = await asyncio.gather(*tasks)

        return extract_results
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/parse")
async def parse_url(item: URLItem):
    async with httpx.AsyncClient() as client:
        try:
            html_content = await fetch_html(client, item.url)
        except HTTPException as e:
            return {"url": item.url, "error": str(e.detail)}
        domain = item.url.split('/')[2]
        parsed_article = parse_article(html_content, domain, item.return_html, item.extra_data)
        return parsed_article


@app.post("/parse_multiple")
async def parse_urls(item: URLListItem):
    async with httpx.AsyncClient() as client:
        tasks = [fetch_html(client, url) for url in item.urls]
        html_contents = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    errors = []

    for url, html_content in zip(item.urls, html_contents):
        if isinstance(html_content, Exception):
            errors.append({"url": url, "error": str(html_content)})
        else:
            domain = url.split('/')[2]
            parsed_article = await parse_article(html_content, domain, item.return_html, item.extra_data)
            if 'error' in parsed_article:
                errors.append(parsed_article)
            else:
                parsed_article["url"] = url
                results.append(parsed_article)

    return {"results": results, "errors": errors}


@app.post("/search_data_for_llm_v2")
async def search_data_for_llm_v2(query: str, sources: Optional[UrlList]):
    """
    You can choose which sources to use by changing body params
    {
      "urls": [
        "ru.wikipedia.org"
      ]
    }
    """
    try:
        # Step 1: Perform the search
        parsed_data = search_func(query, sources.urls)

        # Step 2: Extract content from the search results
        url_list = [item['url'] for item in parsed_data]
        url_list_item = URLListItem(urls=url_list, return_html=False, extra_data=True)

        # Use parse_urls logic to fetch and parse content
        parse_results = await parse_urls(url_list_item)

        return parse_results
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
