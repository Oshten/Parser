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
        if item.find('span', class_='goods-name c-text-sm').get_text(strip=True) == SEARCHED_ELEMENT:
            link = item.get('href')
            prise = item.find('span', class_='price')
            print(link, prise)
            break


def parse():
    html = get_html(url=URL)
    if html.status_code == 200:
        get_content(html=html.text)
    else:
        print('Страница не доступна')

parse()
