from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
from bs4 import BeautifulSoup
from time import sleep
import datetime

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
year = input('請輸入年份')
page=1

odds_url_list = []
game_time_list = []
home_list = []
away_list = []
url = 'https://www.oddsportal.com/baseball/usa/mlb-{}/results/#/page/{}/'.format(year,page)
driver = webdriver.Chrome("./chromedriver.exe",options=options)
#driver.implicitly_wait(10)
html = driver.get(url)
print('等待5秒鐘...')
sleep(5)
html_data = driver.page_source
soup = BeautifulSoup(html_data,'html.parser')
sel_url = soup.select('td[class="name table-participant"] a' )
'''
for i in sel_url :
    half_odds = i['href']
    odds_url_list.append ("https://www.oddsportal.com/"+half_odds+"#over-under;3")

'''
sel_date = soup.select('th[class="first2 tl"] span')
sel_time = soup.select('tr[class="odd deactivate"] td' )

for j in sel_time:
    print(j.text)


#print (odds_url_list)