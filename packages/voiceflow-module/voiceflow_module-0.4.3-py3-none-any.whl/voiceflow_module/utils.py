import requests
import xmltodict
import tiktoken
from typing import Literal


def get_structered_xml(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    response = requests.get(url, headers=headers)
    xml_content = response.content
    parsed_data = xmltodict.parse(xml_content)
    return parsed_data


def split_text_into_chunks(text: str, title: str, url: str, chunk_size=500, overlap=100):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    size = len(tokens)
    step = chunk_size - overlap
    
    chunks = []
    for i in range(0, size, step):
        chunk_tokens = tokens[i:i + chunk_size]
        chunk_text = encoding.decode(chunk_tokens)
        
        chunks.append({
            "Tema": title,
            "Informacija": chunk_text,
            "url": url
        })
    
    return chunks