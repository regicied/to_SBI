# -*- coding: utf-8 -*-
import pandas
import time
import matplotlib.pyplot as plt

PATH = 'C:/PycharmProjects/test_1/gaofzhan/.btctradeCNY.csv'

csv_data = pandas.read_csv(PATH, names=['timestamp', 'price', 'volume'])

csv_data['t_year'] = csv_data['timestamp'].apply(lambda x: time.localtime(x).tm_year)

csv_data['t_month'] = csv_data['timestamp'].apply(lambda x: time.localtime(x).tm_mon)


# 按照年月去对数据进行分组，然后得出volume 最大月份的 年月
df = csv_data.groupby(['t_year', 't_month'])['volume'].sum().reset_index()

t_month = df[df['volume'] == df.max()['volume']]['t_month']

t_year = df[df['volume'] == df.max()['volume']]['t_year']


# 按照上面得出的年月对数据进行筛选
csv_data = csv_data[csv_data['t_year'] == int(t_year)]

csv_data = csv_data[csv_data['t_month'] == int(t_month)]

csv_data['t_day'] = csv_data['timestamp'].apply(lambda x: time.localtime(x).tm_mday)

csv_data['power'] = csv_data['volume'] * csv_data['price']


# 按照day对数据进行分组，然后求得 每天价格的平均值
csv_data = csv_data.groupby(['t_year', 't_month', 't_day']).sum().reset_index()[['t_day', 'power', 'volume']]

csv_data['avg_price'] = csv_data['power'] / csv_data['volume']

price_data = csv_data[['avg_price']]


# 获取数据开始的时间， 然后构造开始时间，画图
min_day = int(csv_data['t_day'].min())

csv_data = csv_data.cumsum()

price_data.index = price_data.index + min_day

t_month = str(t_month) if int(t_month) > 10 else str('0%s' % int(t_month))

min_day = str(min_day) if int(min_day) > 10 else str('0%s' % int(min_day))

start_date = '%s-%s-%s' % (int(t_year), t_month, int(min_day))

price_data.index = pandas.date_range(start_date, periods=len(price_data))

price_data.plot()

plt.show()
