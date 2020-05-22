import pandas as pd
from sqlalchemy import create_engine


host= '1.tcp.jp.ngrok.io:23879'
port= 23879
user= 'eric'
password= 'clubgogo'
db = 'testlala'


engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s") % (user, password, host, db))

try:
    df = pd.read_csv('./Season_data/Season_2010_data.csv',sep=',',index_col=0)
    df.to_sql('game_odds',engine)
    print("Write to MySQL successfully!")
except Exception as e:
    print(e)