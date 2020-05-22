import pymysql
import pandas as pd

# 连接数据库
config = {'host': '1.tcp.jp.ngrok.io',
          'port': 23879,
          'user': 'eric',
          'passwd': 'clubgogo',
          'charset': 'utf8mb4',
          'local_infile': 1
          }

# 建立连接
conn = pymysql.Connect(**config)
# 自动确认commit True
conn.autocommit(1)
# 设置光标
cursor = conn.cursor()
df = pd.read_csv('./Season_data/Season_2010_data.csv', encoding='utf-8', parse_dates=['date'], index_col=0)


# 一个根据pandas自动识别type来设定table的type
def make_table_sql(df):
    columns = df.columns.tolist()
    types = df.ftypes
    # 添加id 制动递增主键模式
    make_table = []
    for item in columns:
        if 'int' in types[item]:
            char = item + ' INT'
        elif 'float' in types[item]:
            char = item + ' FLOAT'
        elif 'object' in types[item]:
            char = item + ' VARCHAR(255)'
        elif 'datetime' in types[item]:
            char = item + ' DATETIME'
        make_table.append(char)
    return ','.join(make_table)

df = pd.read_csv('./Season_data/Season_2010_data.csv', encoding='utf-8', parse_dates=['date'], index_col=0)
# csv 格式输入 mysql 中
def csv2mysql(db_name, table_name, df):
    # 创建database
    # cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    # 选择连接database
    conn.select_db(db_name)
    # 创建table
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    cursor.execute('CREATE TABLE {}({})'.format(table_name, make_table_sql(df)))
    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    df['date'] = df['date'].astype('str')
    values = df.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(df.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, s), values)




