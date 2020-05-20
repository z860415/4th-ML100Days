from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
import concurrent.futures

#虛擬瀏覽器設定
#禁止廣告業面
options = options()
prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
         }
}
options.add_experimental_option('prefs',prefs)
#-----------------------------------------------------------------------------------------------------------
options.add_argument("--headless") #不開啟瀏覽器，於背景執行
options.add_argument('blink-settings=imagesEnabled=false') #不加載圖片
options.add_argument("--disable-javascript") # 禁用JavaScript
#-----------------------------------------------------------------------------------------------------------
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
column_list = ['date','time','team_home','team_away','total','over','under']

print('盤口爬蟲開始執行...')

start_year = int(input('請輸入開始年份'))
end_year = int(input('請輸入結束年份'))+1


#-----------------------------------------------------------------------------------------------------------
for year in range (start_year,end_year):
    start_1 = time.time()
    odds_list1 = pd.read_csv('./Season_url_list/Season_{}_url_list .csv'.format(year), encoding='utf-8', index_col=0).values.tolist()
    odds_list = []
    for i in odds_list1:
        for j in i :
            odds_list.append(j)

    error_list = []
    games_detail = []
    for url in odds_list:
        #第一種網頁格式爬蟲
        start = time.time()
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        driver.get(url)
        driver.implicitly_wait(30)
        html_data = driver.page_source
        soup = BeautifulSoup(html_data, 'html.parser')
        try:
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
            detail_1 = [date_day, date_time, team_home, team_away, total, over_odds, under_odds]
            #確認網頁內容為需要的賠率
            if (float(over_odds) > 2 or float(over_odds) <= 1.8) and len(over_odds) > 1 :
                try:
                    data2 = DataFrame(tables[1])
                    over_odds2 = data2.loc[0, 'Over']
                    under_odds2 = data2.loc[0, 'Under']
                    total2 = data2.loc[0, 'Total']
                    detail_2 = [date_day, date_time, team_home, team_away, total2, over_odds2, under_odds2]
                    games_detail.append(detail_2)
                    print(detail_2)
                except:
                    games_detail.append(detail_1)
                    print(detail_1)
            else:
                games_detail.append(detail_1)
                print(detail_1)
            data = pd.DataFrame(games_detail, columns=column_list)
            data.to_csv("./Season_data/Season_%s_data.csv" % year, encoding='utf_8_sig')

        #解析第二種網頁格式
        except :
            try:
                total = soup.select('div[id="odds-data-table"] a ')[0].text.split('Under ')[1]
                under_odds = soup.select('span[class="avg chunk-odd nowrp"] a ')[0].text
                over_odds = soup.select('span[class="avg chunk-odd nowrp"] a ')[1].text
                team = soup.select('div[id="col-content"] h1')[0].text
                date_all = soup.select('div[id="col-content"] p')[0].text
                team_home = team.split(' - ')[0]
                team_away = team.split(' - ')[1]
                date_day = date_all.split(', ')[1]
                date_time = date_all.split(', ')[2]
                detail_1 = [date_day, date_time, team_home, team_away, total, over_odds, under_odds]

                if float(over_odds) > 2 or float(over_odds) <= 1.8:
                    try:
                        over_odds2 = soup.select('span[class="avg chunk-odd nowrp"] a ')[3].text
                        under_odds2 = soup.select('span[class="avg chunk-odd nowrp"] a ')[2].text
                        total2 = soup.select('div[id="odds-data-table"] a ')[4].text.split('Under ')[1]
                        detail_2 = [date_day, date_time, team_home, team_away, total2, over_odds2, under_odds2]

                        if float(over_odds2) > 2 or float(over_odds2) <= 1.8:
                            try:
                                over_odds3 = soup.select('span[class="avg chunk-odd nowrp"] a ')[5].text
                                under_odds3 = soup.select('span[class="avg chunk-odd nowrp"] a ')[4].text
                                total3 = soup.select('div[id="odds-data-table"] a ')[8].text.split('Under ')[1]
                                detail_3 = [date_day, date_time, team_home, team_away, total3, over_odds3, under_odds3]
                                games_detail.append(detail_3)
                                print(detail_3)
                            except:
                                games_detail.append(detail_2)
                                print(detail_2)
                        else:
                            games_detail.append(detail_2)
                            print(detail_2)

                    except:
                        games_detail.append(detail_1)
                        print(detail_1)

                else:
                    games_detail.append(detail_1)
                    print(detail_1)
            except Exception as e :
                print(e)
                print(url + '網頁異常請確認')
                error_list.append(url)

            data = pd.DataFrame(games_detail, columns=column_list)
            data.to_csv("./Season_data/Season_%s_data.csv" % year, encoding='utf_8_sig')
            error_csv = pd.DataFrame(error_list)
            error_csv.to_csv("./Season_error_list/Season_%s_error_list.csv" % year, encoding='utf_8_sig')

        finally:
            print('虛擬瀏覽器已關閉')
            driver.quit()

        end = time.time()
        print('第%s筆網頁完成，共耗時%s秒'%((len(games_detail)+len(error_list)),end-start))
        a = ((len(games_detail)+len(error_list))/len(odds_list)*100)
        print("當前爬蟲進度{}%".format(a))

    end_1 = time.time()
    print('%s賽季爬蟲完成，共%s筆網頁，耗時%0.2f秒' % (year, (len(games_detail) + len(error_list)), end_1 - start_1))
    print('共' + str(len(error_list)) + '筆網頁異常')








