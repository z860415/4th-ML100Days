from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from pandas import DataFrame

#虛擬瀏覽器設定
options = options()
prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
         }
}
options.add_experimental_option('prefs',prefs)
options.add_argument("--headless") #不開啟瀏覽器，於背景執行



headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
column_list = ['date','time','team_home','team_away','total','over','under']
print('盤口爬蟲開始執行...')


error_list=[]

for year in range (2010,2020):
    # 搜尋總頁數
    odds_url_list = []
    games_detail = []
    print('{}年總網頁搜尋中'.format(year))
    url = 'https://www.oddsportal.com/baseball/usa/mlb-{}/results/#/page/1/'.format(year)
    driver = webdriver.Chrome("./chromedriver.exe", options=options)
    driver.implicitly_wait(10)
    html = driver.get(url)
    html_data = driver.page_source
    driver.close()
    soup = BeautifulSoup(html_data, 'html.parser')
    sel_page_total = int(soup.select('div[id="pagination"] a')[-1]['href'].split('/')[2])


    #爬取總網址
    for a in range (1,2):
        try:
            url = 'https://www.oddsportal.com/baseball/usa/mlb-{}/results/#/page/{}/'.format(year, a)
            driver = webdriver.Chrome("./chromedriver.exe", options=options)
            driver.implicitly_wait(10)
            html = driver.get(url)
            print('第{}頁連結爬取中...'.format(a))
            sleep(5)
            html_data = driver.page_source
            driver.close()
            soup = BeautifulSoup(html_data, 'html.parser')
            sel_url = soup.select('td[class="name table-participant"] a')
            for i in sel_url:
                half_odds = i['href']
                odds_url_list.append("https://www.oddsportal.com" + half_odds + "#over-under;3")
        except:
            break
    print('{}年網頁連結搜尋完成'.format(year))
    print('共'+ str(len(odds_url_list)) + '筆網頁資料')


    # 爬取內文
    for n in odds_url_list:
        try:
            driver = webdriver.Chrome("./chromedriver.exe", options=options)
            driver.implicitly_wait(10)
            html = driver.get(n)
            sleep(5)
            html_data = driver.page_source
            driver.close()
            soup = BeautifulSoup(html_data, 'html.parser')
            tables = pd.read_html(html_data)
            data = DataFrame(tables[0])
            team = soup.select('div[id="col-content"] h1')[0].text
            date_all = soup.select('div[id="col-content"] p')[0].text
            team_home = team.split(' - ')[0]
            team_away = team.split(' - ')[1]
            date_day = date_all.split(', ')[1]
            date_time = date_all.split(', ')[2]
            total = data.loc[0, 'Total']
            over_odds = data.loc[0, 'Over']
            under_odds = data.loc[0, 'Under']
            games_detail.append([date_day,date_time,team_home,team_away,total,over_odds,under_odds])
            print('當前爬蟲進度'+ str(len(games_detail)/len(odds_url_list)) + '...')
        except:
            print(n+'網頁異常請確認')
            error_list.append(n+'網頁異常請確認')
            continue

    print(games_detail)
    print('目前共' + str(len(error_list)) + '筆網頁異常，異常網頁目錄為')
    print(error_list)

    data = pd.DataFrame(games_detail,columns=column_list)
    data.to_csv(f"Season %s.csv"%year, encoding='utf_8_sig')
print(error_list)
print('共' + str(len(error_list)) + '筆網頁異常')
