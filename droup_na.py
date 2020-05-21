from pandas import DataFrame as df
import pandas as pd


column_list = ['date', 'time', 'team_home', 'team_away', 'total', 'over', 'under']
start_year = int(input('請輸入開始年份'))
end_year = int(input('請輸入結束年份'))+1
for year in range(start_year,end_year):
    file = pd.read_csv('./Season_data/Season_{}_data.csv'.format(year), encoding='utf-8',na_values='')
    data = df(file).dropna(axis=0, how='any')
    data.to_csv("./Season_data/Season_{}_data.csv" .format(year), encoding='utf_8_sig',index=0)
    print('資料處理完成')
