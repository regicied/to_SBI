# -*- coding: utf-8 -*-
import csv
import time
import matplotlib.pyplot as plt
from collections import OrderedDict

PATH = 'C:/PycharmProjects/test_1/gaofzhan/.btctradeCNY.csv'


def get_max_mon_data(path):
    """
    因为csv里面的数据按照时间顺序排列，而且数据量不是很大，所以可以通过O(n)时间获得销售额最大月份的数据
    :param path:
    :return: 返回值为 交易量最大月的数据list
    """
    switch = None
    max_mon_total = 0
    now_mon_total = 0
    max_mon_data = None
    now_mon_data = list()
    with open(path, 'r') as f:
        reader = csv.reader(f, dialect='excel')
        for row in reader:
            date, price, volume = row
            date = int(date)
            price = float(price)
            volume = float(volume)
            tm_mon = time.localtime(date).tm_mon
            tm_year = time.localtime(date).tm_year
            if '%s:%s' % (tm_year, tm_mon) != switch:
                switch = '%s:%s' % (tm_year, tm_mon)
                if now_mon_total > max_mon_total:
                    max_mon_data = now_mon_data
                    max_mon_total = now_mon_total
                now_mon_data = list()
                now_mon_total = 0
            if price:
                now_mon_data.append(row)
                now_mon_total += volume
    # 因为数据的最后一个月不会触发 '%s:%s' % (tm_year, tm_mon) != switch 所以需要在循环外进行最后一次比较
    if now_mon_total > max_mon_total:
        max_mon_data = now_mon_data
    return max_mon_data


def draw_picture(data_list):
    x = list()
    y = list()
    mon_data_info = OrderedDict()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for raw in data_list:
        date, price, volume = raw
        mday = time.localtime(int(date)).tm_mday
        daily_info = mon_data_info.setdefault(str(mday), dict(total_volume=0, total_money=0))
        daily_info['total_volume'] += float(volume)
        daily_info['total_money'] += float(volume) * float(price)
    for date, v in mon_data_info.items():
        avg_price = v['total_money'] / v['total_volume']
        x.append(date)
        y.append(avg_price)
    ax.plot(x, y)
    plt.show()


if __name__ == '__main__':
    max_mon_data_list = get_max_mon_data(PATH)
    print 'finish get data'
    draw_picture(max_mon_data_list)
