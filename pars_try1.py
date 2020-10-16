from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

url = 'https://hh.ru/search/vacancy'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
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
        salary = elem.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        if len(salary) > 0:
            if salary.find('-') > -1:
                min_salary = int(salary.split('-')[0].replace(u'\xa0', ''))
                max_salary = int(salary.split('-')[1].split(' ')[0].replace(u'\xa0', ''))
                currency = salary.split('-')[1].split(' ')[1]
            else:
                min_salary = salary.split(' ')[1]
                min_salary = int(min_salary.replace(u'\xa0', ''))
                max_salary = '-'
                currency = salary.split(' ')[-1]
            print('Сайт: hh.ru \t Вакансия: %-40s Зарплата от %6s до %7s %s %s' % (
            name_vacancy, min_salary, max_salary, currency, url_vacancy))
        else:
            print('Сайт: hh.ru \t Вакансия: %-40s Зарплата не определена. %s' % (
            name_vacancy,  url_vacancy))


