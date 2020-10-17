from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient

def get_min_salary():
    print('Введите минимальную зарплату:')
    f = int(input())
    db = client['jobs']
    jobs = db.jobs
    for item in jobs.find({'low_salary': {'$gt': f}}, {'vacancy': True, 'low_salary': True,
                                                       'url': True, '_id': False}):
        print(f'Вакансия: {item["vacancy"]}. Минимальная зарплата: {item["low_salary"]}. Сайт: {item["url"]}')

if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['jobs']
    jobs = db.jobs
    #jobs.delete_many({})
    url = 'https://hh.ru/search/vacancy'
    headers = {'User-Agent':'Mozihttps://hh.ru/search/valla/5.0 (Windows NT'
                            ' 10.0; Win64; x64) AppleWebKit/'
                            '537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    print('Введите профессию:')
    professor = input()
    print('Введите количество страниц для парсинга:')
    pages = int(input())
    for page in range(pages):
        print (f'Страница №{page+1}')
        params = {'clusters': 'true', 'area': 1, 'enable_snippets': 'true', 'salary': '', 'st': 'searchVacancy',
                  'text': professor, 'page': page}
        response = requests.get(url, params=params, headers=headers, verify=False)
        soup = bs(response.text, 'html.parser')
        bloc1 = soup.findAll('div', {'class': 'vacancy-serp-item'})
        for elem in bloc1:
            vacancy = elem.find('a', {'class': 'bloko-link HH-LinkModifier'})
            name_vacancy = vacancy.getText()
            url_vacancy = vacancy['href']
            count_href = len(list(jobs.find({'url': url_vacancy})))
            if count_href > 0:
                print (f'Вакансия {url_vacancy} уже добавлена в базу')
                continue
            salary = elem.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
            min_salary = 0
            max_salary = 0
            currency = 'руб.'
            if len(salary) > 0:
                if salary.find('-') > -1:
                    min_salary = int(salary.split('-')[0].replace(u'\xa0', ''))
                    max_salary = int(salary.split('-')[1].split(' ')[0].replace(u'\xa0', ''))
                    currency = salary.split('-')[1].split(' ')[1]
                else:
                    min_salary = salary.split(' ')[1]
                    min_salary = int(min_salary.replace(u'\xa0', ''))
                    currency = salary.split(' ')[-1]
                print('Сайт: hh.ru \t Вакансия: %-40s Зарплата от %6s до %7s %s %s' % (
                name_vacancy, min_salary, max_salary, currency, url_vacancy))
            else:
                print('Сайт: hh.ru \t Вакансия: %-40s Зарплата не определена. %s' % (
                name_vacancy,  url_vacancy))
            buffer = {'site': 'hh.ru', 'vacancy': name_vacancy, 'low_salary': min_salary,
                      'high_salary': max_salary, 'currency': currency, 'url': url_vacancy}
            jobs.insert_one(buffer)
    url = 'https://russia.superjob.ru/vacancy/search'
    for page in range(1, pages + 1):
        print(f'Страница №{page}')
        params = {'keywords': professor, 'page': page}
        response = requests.get(url, params=params, headers=headers, verify=False)
        # print (response.text)
        soup = bs(response.text, 'html.parser')
        bloc1 = soup.findAll('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
        for elem in bloc1:
            vacancy = elem.find('a', {'class': 'icMQ_'})
            name_vacancy = vacancy.getText()
            url_vacancy = 'https://russia.superjob.ru'+vacancy['href']
            count_href = len(list(jobs.find({'url': url_vacancy})))
            if count_href == 1:
                print(f'Вакансия {url_vacancy} уже добавлена в базу')
                continue
            min_salary = 0
            max_salary = 0
            currency = 'руб.'
            salary = str(elem.find('span', {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'}).getText())
            if salary.find('от') == 0:
                split_salary = salary.split('\xa0')[1:-1]
                currency = salary.split('\xa0')[-1]
                min_salary = ''.join(split_salary)
            elif salary.find('до') == 0:
                split_salary = salary.split('\xa0')[1:-1]
                currency = salary.split('\xa0')[-1]
                max_salary = ''.join(split_salary)
            elif salary.find('—') > 0:
                split_salary = salary.split('—')
                currency = salary.split('\xa0')[-1]
                min_salary = split_salary[0].replace('\xa0', '')
                split_salary_2 = split_salary[1].split('\xa0')[:-1]
                max_salary = ''.join(split_salary_2)
            elif salary == 'По договорённости':
                pass
            else:
                split_salary = salary.split('\xa0')[:-1]
                currency = salary.split('\xa0')[-1]
                min_salary = ''.join(split_salary)
                max_salary = ''.join(split_salary)
            min_salary = int(min_salary)
            max_salary = int(max_salary)
            print('Сайт: superjob.ru \t Вакансия: %-120s Зарплата от %6s до %7s %-20s %s' % (
                name_vacancy, min_salary, max_salary, currency, url_vacancy))

            buffer = {'site': 'superjob.ru', 'vacancy': name_vacancy, 'low_salary': min_salary,
                      'high_salary': max_salary, 'currency': currency, 'url': url_vacancy}
            jobs.insert_one(buffer)
            
    get_min_salary()