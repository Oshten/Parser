import requests
from bs4 import BeautifulSoup

URL = 'https://www.wildberries.ru/brands/polezzno'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36', 'accept' : '*/*'}

SEARCHED_ELEMENT = 'Чай матча зеленая/рассыпной'

def get_html(url, params = None):
    result = requests.get(url=url, headers = HEADERS, params=params)
    return result

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='ref_goods_n_p j-open-full-product-card')
    # print(items)
    for item in items:
        print(item.find('div', slass_='dtlist-inner-brand'))
        break



def parse():
    html = get_html(url=URL)
    if html.status_code == 200:
        get_content(html=html.text)
    else:
        print('Страница не доступна')

parse()
