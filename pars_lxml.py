from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
def pars_yandex():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.75 Safari/537.36'}
    url = 'https://yandex.ru/news'
    response = requests.get(url, headers=headers, verify=False)
    dom = html.fromstring(response.text)
    list_yandex = []
    for item in dom.xpath('//article'):
        name = item.xpath('.//h2/text()')[0]
        link = item.xpath('.//a[@class="news-card__link"]/@href')[0].split('?')[0]
        source = item.xpath('.//span[@class="mg-card-source__source"]/a/text()')[0]
        date = item.xpath('.//span[@class="mg-card-source__time"]/text()')[0]
        buffer = {'name': name, 'link': link, 'source': source, 'date': date}
        list_yandex.append(buffer)
    return list_yandex
def pars_lenta():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.75 Safari/537.36'}
    url = 'https://lenta.ru/parts/news/'
    response = requests.get(url, headers=headers, verify=False)
    dom = html.fromstring(response.text)
    list_lenta = []
    for item in dom.xpath('//div[@class="item news"]'):
        name = item.xpath('.//h3/a/text()')[0].replace('\xa0', ' ')
        link = "https://lenta.ru"+item.xpath('.//h3/a/@href')[0]
        date = item.xpath('.//div[@class="info g-date item__info"]/text()')[0]
        buffer = {'name': name, 'link': link, 'source': "lenta.ru", 'date': date}
        list_lenta.append(buffer)
    return list_lenta
def pars_mail():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.75 Safari/537.36'}
    url = 'https://sportmail.ru/'
    response = requests.get(url, headers=headers, verify=False)
    dom = html.fromstring(response.text)
    list_mail = []
    list_href_mail = []
    for link in dom.xpath('//table//a/@href'):
        list_href_mail.append(link)
    for link in dom.xpath('//li[@class="list__item"]/a/@href'):
        list_href_mail.append(link)
    for item in list_href_mail:
        response1 = requests.get(item, headers=headers, verify=False)
        dom1 = html.fromstring(response1.text)
        name = dom1.xpath('//h1/text()')[0]
        source = dom1.xpath('//a[@class="link color_gray breadcrumbs__link"]/span/text()')[0]
        date = dom1.xpath('//span[@datetime]/@datetime')[0]
        buffer = {'name': name, 'link': item, 'source': source, 'date': date}
        list_mail.append(buffer)
    return list_mail
def write_base(list_all):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    news = db.news
    news.delete_many({})
    news.insert_many(list_all)
    return(news)
if __name__ == '__main__':
    list_all = []
    yandex = pars_yandex()
    list_all.extend(yandex)
    mail = pars_mail()
    list_all.extend(mail)
    lenta = pars_lenta()
    list_all.extend(lenta)
    news = write_base(list_all)
    for item in news.find({}, {'_id': False}):
        print(item)




