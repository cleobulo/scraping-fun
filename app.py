import re
import requests
import config
import urllib.robotparser
import json

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
from datetime import datetime
from database import create_db_and_tables, insert_page, SessionDep

# ============================ Initial Setup
# Define a profundidade máxima desejada
MAX_DEPTH = 2 

# Armazena a URL atual que está sendo processada
NEXT_URL = ''

# TODO_URL_LIST agora armazena tuplas: (url, depth)
TODO_URL_LIST = set()
DONE_URL_LIST = set()

# Cache de parsers de robots.txt por domínio
ROBOTS_CACHE = {}
USER_AGENT = 'MyScraperBotFun'

LIST_FILE = 'todo_list.json'

# ============================ Initial Setup - End
# ============================ Functions
def get_robot_parser(url):
    """Obtém (ou cria) o parser de robots.txt para o domínio da URL."""
    split_url = urlsplit(url)
    domain = f"{split_url.scheme}://{split_url.netloc}"
    
    if domain in ROBOTS_CACHE:
        return ROBOTS_CACHE[domain]
    
    robots_url = f"{domain}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    
    try:
        rp.read()
    except Exception:
        pass
    
    ROBOTS_CACHE[domain] = rp
    
    return rp

def download_page(url):
    """    Faz o download da página HTML de uma URL.
    Se a URL já foi processada, não faz nada.
    """
    if url in DONE_URL_LIST:
        return ''
    # Checa robots.txt antes de baixar
    rp = get_robot_parser(url)
    if rp and not rp.can_fetch(USER_AGENT, url):
        print(f"Bloqueado por robots.txt: {url}")
        DONE_URL_LIST.add(url)
        return ''
    
    # Faz o download da página
    page = requests.get(url)
    DONE_URL_LIST.add(url)
    
    if page.status_code != 200:
        return ''
    
    return page.text

## ============================ Extract Data
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

def extract_title(html):
    """Extrai o título de uma página HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    print(f"Title extracted: {title}")
    return title

def extract_content(html):
    """Extrai o conteúdo principal de uma página HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.get_text(separator=' ', strip=True)
    print(f"Content extracted: {content[:100]}...")  # Print first 100 characters
    return content

## ============================ Extract Data - End

def save_todo_list():
    """    Salva a lista de URLs a serem processadas em um arquivo.
    Pode ser usado para persistência entre execuções."""
    with open('todo_list.json', 'w', encoding='utf-8') as f:
        json.dump(list(TODO_URL_LIST), f, indent=2, ensure_ascii=False)

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
            # TODO: Save data in some database or file
            # TODO: Save the current datetime too
            page_title = extract_title(html)
            page_content = extract_content(html)
            page_scraped_at = datetime.now()
            # Insert page into the database
            with SessionDep() as session:
                insert_page(session, NEXT_URL, page_title, page_content, page_scraped_at)
            # Log the scraping action with timestamp
            print(f"Scraped: {NEXT_URL} (depth {depth}) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("==========================")
        except Exception as e:
            print(f"Erro ao processar {NEXT_URL}: {e}")

def main():
    try:
        seed_url = config.get_url_from_arg()
        TODO_URL_LIST.add((seed_url, 0))
        create_db_and_tables()  # Ensure database and tables are created
        start_scraping()
    except KeyboardInterrupt:
        save_todo_list()  # Save the current state of TODO_URL_LIST
        print('*')
        print('bye!')

# ============================ Functions - End
# ============================ Main Execution
if __name__ == '__main__':
    main()
else:
    print('This script is not meant to be imported as a module.')
    print('Please run it directly from the command line.')
    exit(1)
