from datetime import datetime
import datetime
from pandas import DataFrame as df
import pandas as pd


start_year = int(input('請輸入開始年份'))
end_year = int(input('請輸入結束年份'))+1
for year in range(start_year,end_year):

    data = pd.read_csv('./Season_data/Season_{}_data.csv'.format(year), header=0)

    for i in range(0, len(data)):
        row = data.iloc[i]['date']
        a = row
        dateString = a
        dateFormatter = "%d %b  %Y"
        b = datetime.datetime.strptime(dateString, dateFormatter)
        targetDate = b.strftime("%Y-%m-%d")
        data.loc[i,'date'] = targetDate
    data.to_csv("./Season_data/Season_{}_data.csv".format(year), encoding='utf_8_sig', index=0)
    print('{}年日期修改完成'.format(year))