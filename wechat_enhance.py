#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2020-12-07
@author: Shell.Xu
@copyright: 2020, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
@comment:
微信增强工具主要解决微信扣款时，目标商户细节不穿透导致的问题。没有增强数据的情况下，银行数据无法帮助分辨消费。
进入微信账单，选择“常见问题”，“下载账单”，“用于个人对账”。最长可以选择三个月。
账单会发送到邮箱，密码在微信中可以看到。解密后将csv文件放置在wechat路径下。
执行脚本，输入为其他账单输出。如果输出项目的日期，卡号，金额全部一致，微信账单细节将替换原始细节。
'''
import re
import sys
import csv
import gzip
import glob
import datetime


re_card = re.compile(r'.*\((\d{4})\)')


def main():
    wechat_info = {}
    for fn in glob.glob('wechat/微信支付账单*.csv.gz'):
        with gzip.open(fn, 'rt', encoding='utf-8') as fi:
            for row in csv.reader(fi):
                try:
                    dt = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    date = dt.strftime('%Y%m%d')
                except ValueError:
                    continue
                if row[4] == '收入':
                    continue
                if row[6] == '零钱':
                    continue
                m_card = re_card.match(row[6])
                if not m_card:
                    # raise Exception(row[6])
                    continue
                wechat_info[(date, m_card.groups()[0], row[5].strip('¥'))] = row[2]

    writer = csv.writer(sys.stdout)
    for row in csv.reader(sys.stdin):
        desc = wechat_info.get((row[1], row[2], row[3]))
        if desc:
            writer.writerow([row[i] for i in range(4)] + ['微信:'+desc,])
        else:
            writer.writerow(row)


if __name__ == '__main__':
    main()
