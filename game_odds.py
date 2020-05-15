from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
from bs4 import BeautifulSoup
from time import sleep
import datetime
'''
start = input('請輸入開始日期ex:2020-05-13')
end = input('請輸入結束日期ex:2020-05-13')
datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
dateend=datetime.datetime.strptime(end,'%Y-%m-%d')

while datestart<dateend:
    datestart+=datetime.timedelta(days=1)
    print(datestart.strftime('%Y%m%d'))
'''
options = options()
prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
         }
}
options.add_experimental_option('prefs',prefs)
options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
#options.add_argument("--start-maximized")     #最大化視窗
#options.add_argument("--incognito")           #開啟無痕模式


url = 'https://www.oddsportal.com/baseball/usa/mlb-2010/milwaukee-brewers-miami-marlins-fsukEpis/#over-under;3'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
driver = webdriver.Chrome("./chromedriver.exe",options=options)
driver.implicitly_wait(10)
html = driver.get(url)
sleep(5)
#wait = WebDriverWait(webdriver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'_3Nv_7')))
html_data = driver.page_source
soup = BeautifulSoup(html_data,'html.parser')
sel_1 = soup.select('td[class="center"]')
#sel_2 = soup.select('div[class="_3A-gC _2DWLf _3zKaX _1BrlL"]')
for i in sel_1:
    print(i.text)
print('=====================')
#for n in sel_2:
#    print(n.text)