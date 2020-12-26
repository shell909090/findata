#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2020-12-26
@author: Shell.Xu
@copyright: 2020, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
@comment:
输入和输出都是标准账簿。寻找账簿内日期和卡号相同，大小相反的多笔记录并对应消除。
注意一：有可能花销两笔，退款一笔。消除完毕需要留一笔退款。
注意二：花销和退款的注释可能不同。
'''
import sys
import csv
import decimal
import collections


def src_cnt(data):
    for row in data:
        yield row[1], row[2], decimal.Decimal(row[3])


def main():
    data = []
    writer = csv.writer(sys.stdout)

    data = [row for row in csv.reader(sys.stdin)]
    cnt = collections.Counter(src_cnt(data))

    for row in data:
        rev_idx = (row[1], row[2], -decimal.Decimal(row[3]))
        if rev_idx not in cnt:
            writer.writerow(row)
            continue
        cnt[rev_idx] -= 1
        if cnt[rev_idx] == 0:
            del cnt[rev_idx]


if __name__ == '__main__':
    main()
