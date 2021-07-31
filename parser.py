import requests
from bs4 import BeautifulSoup

URL = 'https://www.wildberries.ru/brands/polezzno'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36', 'accept' : '*/*'}


def get_html(url, params = None):
    result = requests.get(url=url, headers = HEADERS, params=params)
    return result

def parse():
    html = get_html(url=URL)
    if html.status_code == 200:
        pass
    else:
        print('Страница не доступна')

parse()
