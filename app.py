import re
import requests
import args

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit

# Define a profundidade máxima desejada
MAX_DEPTH = 2 

# Armazena a URL atual que está sendo processada
NEXT_URL = ''

# TODO_URL_LIST agora armazena tuplas: (url, depth)
TODO_URL_LIST = set()
DONE_URL_LIST = set()

def download_page(url):
    """    Faz o download da página HTML de uma URL.
    Se a URL já foi processada, não faz nada.
    """
    if url in DONE_URL_LIST:
        return ''
    
    page = requests.get(url)
    DONE_URL_LIST.add(url)
    
    if page.status_code != 200:
        return ''
    
    return page.text

def extract_internal_links(html, next_url, depth):
    """    Extrai links internos de uma página HTML.
    Se a profundidade máxima for atingida, não faz nada.
    """
    if depth >= MAX_DEPTH:
        return
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    split_next_url = urlsplit(next_url)
    base_next_url = f'{split_next_url.scheme}://{split_next_url.netloc}'
    for link in links:
        if 'href' in link.attrs:
            href = link.attrs['href']
            if re.match(r'^/\w+', href):
                new_url = urljoin(base_next_url, href)
                if new_url not in DONE_URL_LIST:
                    TODO_URL_LIST.add((new_url, depth + 1))

def extract_external_links(html, next_url, depth):
    """    Extrai links externos de uma página HTML.
    Se a profundidade máxima for atingida, não faz nada."""
    if depth >= MAX_DEPTH:
        return
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    split_next_url = urlsplit(next_url)
    base_next_url = f'{split_next_url.scheme}://{split_next_url.netloc}'
    for link in links:
        if 'href' in link.attrs:
            href = link.attrs['href']
            if re.match(r'^https?://', href) and not href.startswith(base_next_url):
                new_url = href
                if new_url not in DONE_URL_LIST:
                    TODO_URL_LIST.add((new_url, depth + 1))

def start_scraping():
    """    Inicia o processo de scraping, processando URLs na lista TODO_URL_LIST.
    Continua até que não haja mais URLs a serem processadas."""
    while TODO_URL_LIST:
        NEXT_URL, depth = TODO_URL_LIST.pop()
        if NEXT_URL in DONE_URL_LIST:
            continue
        try:
            html = download_page(NEXT_URL)
            extract_internal_links(html, NEXT_URL, depth)
            extract_external_links(html, NEXT_URL, depth)
            print(f"Scraped: {NEXT_URL} (depth {depth})")
        except Exception as e:
            print(f"Erro ao processar {NEXT_URL}: {e}")

def main():
    try:
        seed_url = args.get_url_from_arg()
        TODO_URL_LIST.add((seed_url, 0))
        start_scraping()
    except KeyboardInterrupt:
        print('*')
        print('bye!')

if __name__ == '__main__':
    main()
else:
    print('This script is not meant to be imported as a module.')
    print('Please run it directly from the command line.')
    exit(1)
