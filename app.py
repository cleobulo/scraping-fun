import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://python.org'
NEXT_URL = ''
TODO_URL_LIST = set([BASE_URL])
DONE_URL_LIST = set()

def download_page(url):
    page = requests.get(url)
    DONE_URL_LIST.add(url)
    
    return page.text

def extract_internal_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    
    for link in links:
        if 'href' in link.attrs:
            href = link.attrs['href']

            if re.match('^/\w+', href):
                new_url = urljoin(BASE_URL, href)
                
                if new_url not in DONE_URL_LIST:
                    TODO_URL_LIST.add(new_url)

def main():
    NEXT_URL = TODO_URL_LIST.pop()
    while NEXT_URL not in DONE_URL_LIST:
        html = download_page(NEXT_URL)
        extract_internal_links(html)
        print(NEXT_URL)
        NEXT_URL = TODO_URL_LIST.pop()
try:
    main()
except KeyboardInterrupt:
    print('*')
    print('bye!')
