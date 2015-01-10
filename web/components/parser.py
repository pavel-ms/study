from tornado.httpclient import HTTPClient, HTTPRequest, AsyncHTTPClient
from bs4 import BeautifulSoup
from web.models import Car
import re


class ParserHelper:
    """
    Функции помощники при парсинге страниц
    """
    def extract_int(self, val):
        ls = [s for s in val.split() if s.isdigit()]
        val = ''
        for item in ls:
            val += item
        return val

    def extract_model_from_title(self, title):
        val = ''
        r = re.compile(u'^Купить\s+([-a-zA-Zа-яёА-ЯЁ\s]+)\s+с', re.U)
        match = r.search(title)
        if match:
            val = match.group(1)
        return val

    def fetch_ext_id(self, link):
        val = ''
        r = re.compile(r'\/(\d+)-[a-z0-9]+\/')
        match = r.search(link)
        if match:
            val = match.group(1)
        return int(val)


class Parser:
    """
    Непосредственно класс парсера сайта
    """
    def __init__(self):
        # http клиент для парсинга сайтов
        self._client = HTTPClient()
        # мы ищем только инфинити, поэтому и будем отталкиваться только от этой страницы
        self._base_url = 'http://auto.ru/cars/infiniti/g/iv/group-coupe/used/'
        self._helper = ParserHelper()

    def parse(self):
        """
        Запускает процесс парсинга страниц
        """
        links = self.get_links()
        r = self.parse_links(links)
        return r

    def get_links(self):
        """
        Получаем все ссылки на карточки товаров с исходной страницы
        """
        request = HTTPRequest(self._base_url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        })
        response = self._client.fetch(request)
        html = response.body
        parser = BeautifulSoup(html)
        links = parser.select('a.sales-link')
        return [l.attrs['href'] for l in links]

    def parse_links(self, links):
        """
        Получаем данные всех карточек продуктов,
        которые были на исходной странице
        """
        models = []
        http = HTTPClient()
        for l in links:
            request = HTTPRequest(l, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            })
            res = http.fetch(request)
            data = self.handle_response(res.body.decode('utf-8'), l)
            models.append(self.create_model(data))
        return models

    def handle_response(self, html, link):
        """
        Парсим html странички карточки товара
        @return array of dict
        """
        soup = BeautifulSoup(html)
        # with open('test.html', 'w') as f:
        #     f.write(str(soup.prettify()))
        data = {}

        data['external_id'] = self._helper.fetch_ext_id(link)

        title = soup.select('title')[0].getText()
        data['model'] = self._helper.extract_model_from_title(title)

        data['cover'] = soup.select('.b-fotorama-photo-img')[0].attrs['src']

        price = soup.select('span[itemprop=price]')[0].getText()
        data['price'] = self._helper.extract_int(price)

        data['descr'] = str(soup.select('.card-details-text-shadow')[0])

        return data

    def create_model(self, data):
        """
        Создаем модель по данным с карточки товара
        """
        try:
            model = Car.objects.get(external_id=data['external_id'])
        except Car.DoesNotExist:
            model = None

        if model:
            pass
        else:
            model = Car(
                external_id=data['external_id']
                , model=data['model']
                , cover=data['cover']
                , price=data['price']
                , descr=data['descr']
            )
            model.save()

        return model