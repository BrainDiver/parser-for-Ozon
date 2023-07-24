from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from fake_useragent import UserAgent

#Эту программу лучше бы было сделать с помощью aiohttp или httpx и я получил бы результат быстрее но я решил попрактиковатся и сделать ее с помощью Selenium 


#Подключаю driver, headers и опции 
useragent=UserAgent()
options=Options()
service=Service("./chromedriver")
#Добавляю в опции свои настройки а именно отключаю контроль автоматизации, устанавливаю случайные выбор заголовков из библиотеки fake_useragent, открываю браузер на весь экран
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-agent='HelloWorld'")
options.add_argument("start-maximized")
#options.add_argument("--headless")


#спрашиваю пользователя нужны ли прокси и прошу ввести запрос для поиска
proxy_query=input("Enter proxy if they need, example IP:PORT ")
query=input("Enter search query ")

#Проверяю задан ли прокси и если задан добавляю его в качестве аргумента в опции
if len(proxy_query):
    options.add_argument(f"--proxy-server=46.148.34.7:8080")
else:
    pass


driver=webdriver.Chrome(service=service, options=options)
url="http://Ozon.ru"
try:
    driver.get(url)
    sleep(30)
except Exception as err:
    print(err)
finally:
    driver.close()
    driver.quit()
