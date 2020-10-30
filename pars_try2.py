from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
#https://russia.superjob.ru/vacancy/search/?keywords=%D0%92%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F
url = 'https://russia.superjob.ru/vacancy/search'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
print('Введите профессию:')
professor = input()
print('Введите количество страниц для парсинга:')
pages = input()
pages = int(pages)
for page in range(1, pages+1):
    print(f'Страница №{page}')
    params = {'keywords': professor, 'page': page}
    response = requests.get(url, params=params, headers=headers, verify=False)
    #print (response.text)
    soup = bs(response.text, 'html.parser')
    bloc1 = soup.findAll('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
    for elem in bloc1:
        vacancy = elem.find('a', {'class': 'icMQ_'})
        name_vacancy = vacancy.getText()
        url_vacancy = vacancy['href']
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


