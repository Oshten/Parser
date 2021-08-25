from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from Utime import time_coute

URL_WILDBERRIES = 'https://www.wildberries.ru/brands/polezzno'
URL_VAMPOLEZNO = 'https://vampolezno.com/polezzno/'
URL_FOURFRESH = 'https://4fresh.ru/catalog/food'


HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36', 'accept' : '*/*'}

# SEARCHED_ELEMENT = ('Чай матча зеленая/рассыпной', 'Чай матча голубая', 'Кисель')
# # searched_element = SEARCHED_ELEMENT[2]
searched_element = 'матча'

HOST_WILDBERRIES = 'https://www.wildberries.ru'
HOST_VAMPOLEZNO = 'https://vampolezno.com'
HOST_FOURFRESH = 'https://4fresh.ru'

FILE = 'Информация о ценах.txt'

class Parser:

    def __init__(self, url, shope_name, find_product):
        self.find_product = find_product
        self.shope_name = shope_name
        self.headers = HEADERS
        self.file = FILE
        self.url = url
        self.params = None
        self.html = None
        self.contents = None
        self.prise = None
        self.product = None
        self.link_product = None
        self.link = None


    def run(self):
        self.html = requests.get(url=self.url, headers=self.headers, params=self.params)
        if self.html.status_code == 200:
            print(1)
            self.get_content()
            self.search_product()
            self.find_next_url()
            # print(self.link)
            if self.link and self.link != self.url:
                parser = Parser(url=self.link, shope_name=self.shope_name, find_product=self.find_product)
                parser.run()
            else:
                print('Все страницы проверены')
        else:
            print(f'Страница {self.url} не доступна')

    def get_content(self):
        print(f'Идет парсинг страницы {self.url} ...')
        self.contents = BeautifulSoup(self.html.text, 'html.parser')
        # print(self.contents)

    def record_info(self):
        with open(self.file, 'a', encoding='utf8') as file:
            file.write(f'{self.shope_name}\n{self.product}\n{self.prise}\n{self.link_product}\n\n\n\n')


    def search_product(self):
        pass

    def find_next_url(self):
        pass

class ParserWaldberries(Parser):

    def search_product(self):
        items = self.contents.find_all('a', class_='product-card__main')
        # print(items)
        for item in items:
            # print(item.find('span', class_='goods-name').get_text(strip=True))
            if self.find_product in item.find('span', class_='goods-name').get_text(strip=True):
                self.product = item.find('span', class_='goods-name').get_text(strip=True)
                # print(self.product)
                self.link_priduct = urljoin(base=HOST_WILDBERRIES, url=item.get('href'))
                print(self.link_product)
                self.prise = item.find('span', class_='price').get_text(strip=True)
                # print(self.prise)
                print(f'Товар на сайте {self.shope_name} найден.')
                self.record_info()

    def find_next_url(self):
        # print(self.contents)
        # self.contents.find('a', class_='pagination-item').get_text()
        try:
            self.link = urljoin(base=HOST_WILDBERRIES,
                                url=self.contents.find('a', class_='catalog-pagination__next').get('href'))
            print(self.link)
        except AttributeError:
            self.link = None

class ParserFourfresh(Parser):

    def __init__(self, url, shope_name, find_product, params):
        super().__init__(url, shope_name, find_product)
        self.params = params
        self.produkt_coul = 192

    def search_product(self):
        items = self.contents.find_all('article', class_='prod-card-small')
        for item in items:
            # print(item.find('a', class_='ci-list-item__name').get_text(strip=True))
            if self.find_product in item.find('a', class_='ci-list-item__name').get_text(strip=True):
                self.product = item.find('a', class_='ci-list-item__name').get_text(strip=True)
                self.link_product = urljoin(HOST_FOURFRESH, item.find('a').get('href'))
                self.prise = item.find('div', class_='ci-actual-price').get_text(strip=True)
                print(f'Товар на сайте {self.shope_name} найден.')
                # print(link, prise)
                self.record_info()

    def find_next_url(self):
        self.link = urljoin(HOST_FOURFRESH, self.contents.find('a', class_='next').get('href'))

    def run(self):
        self.html = requests.get(url=self.url, headers=self.headers, params=self.params)
        if self.html.status_code == 200:
            self.get_content()
            self.search_product()
        else:
            print(f'Страница {self.url} не доступна')




# parser_waldberris = ParserWaldberries(url = URL_WILDBERRIES,
#                                       shope_name='Wildberries',
#                                       find_product=searched_element)
# parser_waldberris.run()


@time_coute
def parsers(url, shope_name, find_product):
    for page in range(1, 193):
        params = 'PAGEN_1=' + str(page)
        print(f'Идет парсинг страницы {page} ...')
        parser_fourfresh = ParserFourfresh(url=url,
                                          shope_name=shope_name,
                                          find_product=find_product, params=params)
        parser_fourfresh.run()


parsers(url = URL_FOURFRESH, shope_name='Fourfresh', find_product=searched_element)


