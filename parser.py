import os
import requests
from bs4 import BeautifulSoup

URL_WILDBERRIES = 'https://www.wildberries.ru/brands/polezzno'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36', 'accept' : '*/*'}

SEARCHED_ELEMENT = ('Чай матча зеленая/рассыпной', 'Чай матча голубая', 'Кисель')
searched_element = SEARCHED_ELEMENT[2]

HOST_WILDBERRIES = 'https://www.wildberries.ru'

FILE = 'Информация о ценах.txt'

def get_html(url, params = None):
    result = requests.get(url=url, headers = HEADERS, params=params)
    return result

def get_pagination_next(html):
    soup = BeautifulSoup(html, 'html.parser')
    page_next = HOST_WILDBERRIES + soup.find('a', class_='pagination-next').get('href')
    return page_next

def get_content(html):
    print('Идет парсинг ...')
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='ref_goods_n_p j-open-full-product-card')
    for item in items:
        # print(item.find('span', class_='goods-name').get_text(strip=True))
        if item.find('span', class_='goods-name').get_text(strip=True) == searched_element:
            # print(item.find('span', class_='goods-name').get_text(strip=True))
            link = HOST_WILDBERRIES + item.get('href')
            prise = item.find('span', class_='price').get_text(strip=True)
            print(f'Товар на сайте {HOST_WILDBERRIES} найден.')
            # print(link, prise)
            return prise, link
    else:
        return False



def record_info(file_info, prise, link):
    with open(file_info, 'a', encoding='utf8') as file:
        shope_name = HOST_WILDBERRIES.split('.')[1]
        file.write(shope_name + '\n' + searched_element + '\n' + prise + '\n' + link + '\n' + '\n\n\n')


def parse():
    html = get_html(url=URL_WILDBERRIES)
    if html.status_code == 200:
        while True:
            try:
                prise, link = get_content(html=html.text)
                break
            except TypeError:
                try:
                    page_next = get_pagination_next(html=html.text)
                    html = get_html(url=page_next)
                except AttributeError:
                    print(f'Товар на сайте {HOST_WILDBERRIES} не найден.')
                    prise, link = 'Товар отсутствует', 'Товар отсутствует'
                    break
        record_info(file_info=FILE, prise=prise, link=link)
    else:
        print('Страница не доступна')


parse()

# url = 'https://www.wildberries.ru/brands/polezzno'
# html = get_html(url=url, params='page=1')
# prise, link = get_content(html=html.text)
# print(prise, link)
# print(get_pagination_next(html=html.text))