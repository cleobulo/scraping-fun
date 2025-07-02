import re
import requests
import args

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit

NEXT_URL = ''
TODO_URL_LIST = set([])
DONE_URL_LIST = set()

def download_page(url):
    page = requests.get(url)
    DONE_URL_LIST.add(url)
    
    return page.text

def extract_internal_links(html, next_url):
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
                    TODO_URL_LIST.add(new_url)

def start_scraping():
    NEXT_URL = TODO_URL_LIST.pop()
    while NEXT_URL not in DONE_URL_LIST:
        html = download_page(NEXT_URL)
        extract_internal_links(html, NEXT_URL)
        print(f"Scraped: {NEXT_URL}")
        NEXT_URL = TODO_URL_LIST.pop()

def main():
    try:
        seed_url = args.get_url_from_arg()
        TODO_URL_LIST.add(seed_url)
        start_scraping()
    except ValueError as e:
        print(f'Error: {e}')
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
