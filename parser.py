import os
import requests
from bs4 import BeautifulSoup

URL_WILDBERRIES = 'https://www.wildberries.ru/brands/polezzno'
URL_VAMPOLEZNO = 'https://vampolezno.com/polezzno/'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36', 'accept' : '*/*'}

# SEARCHED_ELEMENT = ('Чай матча зеленая/рассыпной', 'Чай матча голубая', 'Кисель')
# # searched_element = SEARCHED_ELEMENT[2]
searched_element = 'матча'

HOST_WILDBERRIES = 'https://www.wildberries.ru'
HOST_VAMPOLEZNO = 'https://vampolezno.com'

FILE = 'Информация о ценах.txt'

def get_html(url, params = None):
    result = requests.get(url=url, headers = HEADERS, params=params)
    return result

def get_pagination_next(html, host):
    soup = BeautifulSoup(html, 'html.parser')
    page_next = host + soup.find('a', class_='pagination-next').get('href')
    return page_next

def record_info(prise, link, shop_name, produkt):
    with open(FILE, 'a', encoding='utf8') as file:
        # shope_name = host.split('.')[1]
        file.write(shop_name + '\n' + produkt + '\n' + prise + '\n' + link + '\n' + '\n\n\n')

def get_content_waldberries(html):
    print('Идет парсинг ...')
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='ref_goods_n_p j-open-full-product-card')
    for item in items:
        # print(item.find('span', class_='goods-name').get_text(strip=True))
        if searched_element in item.find('span', class_='goods-name').get_text(strip=True):
            produkt = item.find('span', class_='goods-name').get_text(strip=True)
            # print(item.find('span', class_='goods-name').get_text(strip=True))
            link = HOST_WILDBERRIES + item.get('href')
            prise = item.find('span', class_='price').get_text(strip=True)
            print(f'Товар на сайте {HOST_WILDBERRIES} найден.')
            record_info(prise=prise, link=link, shop_name='Wildberries', produkt=produkt)

def parse_waldberries(url, func):
    html = get_html(url=url)
    if html.status_code == 200:
        while True:
            func(html=html.text)
            try:
                page_next = get_pagination_next(html=html.text, host=HOST_WILDBERRIES)
                html = get_html(url=page_next)
            except AttributeError:
                print('Все страницы проверены')
                break
    else:
        print('Страница не доступна')

def get_content_vampolezno(html):
    print('Идет парсинг ...')
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='tabs-shadow-category')
    for item in items:
        # print(item.find('h5').get_text(strip=True))
        if searched_element in item.find('h5').get_text(strip=True):
            produkt = item.find('h5').get_text(strip=True)
            link = HOST_VAMPOLEZNO + item.find('a').get('href')
            prise = item.find('div', class_='pricing radiocard prcb-single').get_text(strip=True)
            print(f'Товар на сайте {HOST_VAMPOLEZNO} найден.')
            record_info(prise=prise, link=link, shop_name='Vampolezno', produkt=produkt)

def parse_vampolezno(url, func, host):
    html = get_html(url=url)
    if html.status_code == 200:
        while True:
            func(html=html.text)
            try:
                page_next = get_pagination_next(html=html.text, host=host)
                html = get_html(url=page_next)
            except AttributeError:
                print('Все страницы проверены')
                break
    else:
        print('Страница не доступна')




parse_waldberries(url = URL_WILDBERRIES, func=get_content_waldberries)
parse_vampolezno(url = URL_VAMPOLEZNO, func=get_content_vampolezno, host=HOST_VAMPOLEZNO)

# url = URL_VAMPOLEZNO
# html = get_html(url=url, params=None)
# get_content_next(html=html.text)

# print(prise, link)
# print(get_pagination_next(html=html.text))