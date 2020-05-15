from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
from bs4 import BeautifulSoup
from time import sleep
import datetime
import pandas as pd

options = options()
prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
         }
}
options.add_experimental_option('prefs',prefs)
options.add_argument("--headless")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
year = 2010 #input('請輸入年份')
page=1
url = 'https://www.baseball-reference.com/boxes/HOU/HOU201910300.shtml'
driver = webdriver.Chrome("./chromedriver.exe",options=options)
#driver.implicitly_wait(10)
html = driver.get(url)
sleep(5)
html_data = driver.page_source
#soup = BeautifulSoup(html,'html.parser')
tables = pd.read_html(html_data)
print(tables[9])


tables[9].to_csv('tt.csv',encoding='utf-8-sig')