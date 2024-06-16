from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import urllib.parse
import requests
import aiohttp
import asyncio
from typing import List, Optional
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from config import config

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

async def get_page_content(url):
    try:
        REQUEST_HEADERS = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=REQUEST_HEADERS) as response:
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
    except aiohttp.ClientError as e:
        return {
            "url": url,
            "error": str(e)
        }

def search_func(query: str, sources: List[str]):
    try:
        encoded_query = urllib.parse.quote(query)
        if sources and sources.urls:
            encoded_query = ["site:" + urllib.parse.quote(url)+f"%20{encoded_query}" for url in sources.urls]
            encoded_query = "%20|%20".join(encoded_query)

        yandex_url = f"https://yandex.ru/search/xml?folderid={config.yandex.folderid}&apikey={config.yandex.apikey}&query={encoded_query}"        
        response = requests.get(yandex_url)
        xml_data = response.text
        parsed_data = parse_yandex_xml(xml_data)
        return parsed_data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search(query: str, sources: Optional[UrlList]):
    '''
```
    You can choose which sources to use by changing body params
    {
      "urls": [
        "ru.wikipedia.org"
      ]
    }
```
    '''
    return search_func(query, sources)
    
@app.post("/extract", response_model=List[dict])
async def extract(url_list: UrlList):
    '''
```
    Pass the urls for text extracting
    {
      "urls": [
        "ru.wikipedia.org"
      ]
    }
```
    '''
    if not isinstance(url_list.urls, list):
        raise HTTPException(status_code=400, detail="URLs should be provided as a list")

    tasks = [get_page_content(url) for url in url_list.urls]
    results = await asyncio.gather(*tasks)
    return results

@app.post("/search_data_for_llm")
async def search_data_for_llm(query: str, sources: Optional[UrlList]):
    '''
```
    You can choose which sources to use by changing body params
    {
      "urls": [
        "ru.wikipedia.org"
      ]
    }
```
    '''
    try:
        # Step 1: Perform the search
        parsed_data = search_func(query, sources)

        # Step 2: Extract content from the search results
        url_list = [item['url'] for item in parsed_data]
        tasks = [get_page_content(url) for url in url_list]
        extract_results = await asyncio.gather(*tasks)

        return extract_results
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
