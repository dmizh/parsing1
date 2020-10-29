from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time

driver = webdriver.Firefox(executable_path="/home/user/PycharmProjects/geckodriver")
driver.maximize_window()
driver.get('https://mail.ru/')
login = driver.find_element_by_id('mailbox:login-input')
login.send_keys('study.ai_172@mail.ru')
button = driver.find_element_by_id('mailbox:submit-button')
button.click()
time.sleep(5)
password = driver.find_element_by_id('mailbox:password-input')
password.send_keys('NextPassword172')
button = driver.find_element_by_id('mailbox:submit-button')
button.click()
time.sleep(15)

#while True:
 #   letters = driver.find_elements_by_class_name('js-letter-list-item')
  #  actions = ActionChains(driver)
   # actions.move_to_element(letters[-1])
    #last_link = letters[-1].get_attribute('href')
    #actions.perform()
    #time.sleep(10)
    #new_last_link = letters[-1].get_attribute('href')
    #if last_link == new_last_link:
    #break

letters = driver.find_elements_by_class_name('js-letter-list-item')
list_letters = []
list_mail = []

for letter in letters:
    list_letters.append(letter.get_attribute('href'))

for url in list_letters:
    driver.get(url)
    time.sleep(10)
    author = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    when = driver.find_element_by_class_name('letter__date').text
    context = driver.find_element_by_class_name('thread__subject').text
    material = driver.find_element_by_class_name('letter__body').text
    buffer = {'author': author, 'time': when, 'context': context, 'text': material}
    list_mail.append(buffer)

client = MongoClient('127.0.0.1', 27017)
db = client['letters']
letters_mail = db.letters_mail
letters_mail.delete_many({})
letters_mail.insert_many(list_mail)
for item in letters_mail.find({}, {'_id': False}):
    print(item)






