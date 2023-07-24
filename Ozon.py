import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from fake_useragent import UserAgent
from dataclasses import dataclass
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Этот парсер лучше бы было сделать с помощью aiohttp или httpx и скорость выполнения была бы намного быстрее но я решил попрактиковатся и сделать его с помощью Selenium


#Подключаю driver, headers и опции 
useragent=UserAgent()
options=uc.ChromeOptions()
service=Service("./chromedriver")
#Добавляю в опции свои настройки а именно отключаю контроль автоматизации, устанавливаю случайные выбор заголовков из библиотеки fake_useragent, открываю браузер на весь экран
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-agent={useragent.random}")
options.add_argument("start-maximized")
#options.add_argument("--headless")
query=input("Enter search query ")
print("Okey Lets GO!\n"
      "This program using undetected chromedriver(long to load), query can take some time. Don't do anything just wait near minute")

@dataclass
class Products:
    link: str
    name: str
    description: str
    price: str
    
    def to_dict(self):
        return {"link": self.link, "title": self.name, "description": self.description, "price": self.price}

#Открываю браузер 
driver=uc.Chrome(service=service, options=options)
driver.delete_all_cookies()
#задаю переменную с адрессом сайта
url="https://www.ozon.ru"
try:
    #Открываю сайт 
    driver.get(url)
    first_sleep= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "y1v.tsBodyL")))
    #Нахожу поле для поиска и очищаю его
    print('Start search')
    search=driver.find_element(By.CLASS_NAME, "y1v.tsBodyL")
    search.clear()
    #Ввожу запрос который ввел пользователь и начинаю поиск
    search.send_keys(query)
    search.send_keys(Keys.ENTER)
    second_sleep= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "ni0")))
    #Нахожу на странице все нужные мне элементы и циклом получаю информацию 
    elements=driver.find_elements(By.CLASS_NAME, "ni0")
    elements_price=driver.find_elements(By.CLASS_NAME, "d6-a0")
    product_item=[]
    sleep(100)
    for element in elements:
        element_href=element.find_element(By.CLASS_NAME, "tile-hover-target.i7j.ij8").get_attribute("href")
        element_title=element.find_element(By.CLASS_NAME, "du4.ud4.du5.du7.tsBodyL.i7j.ij8").get_attribute("textContent")
        element_description=element.find_element(By.CLASS_NAME, "du4.ud4.du8.tsBodyM.i7j").get_attribute("textContent")
        #чтобы не бежать по второму списку циклом и поскольку элементы второго списка находятся в том же порядке что и в первом и каждый элемент второго списка соответствуют каждому элементу первого, я просто использую индекс элемента первого списка для получения нужного мне элемента из второго 
        index_=elements.index(element)
        if index_ < len(elements_price):
            element_price=elements_price[index_].get_attribute("textContent")
        else:
            pass
        result=Products(link=element_href, name=element_title, description=element_description, price=element_price[:-1].replace("\u2009", '')+" Руб")
        print(result)
        product_item.append(result.to_dict())
    sleep(5)
    print(product_item)
    print("Done")
except Exception as error:
    #Вывожу исключение на экран
	print(error)
finally:
    #Заканчиваю выполнение программы
    driver.close()
    driver.quit()
