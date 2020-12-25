#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2020-12-02
@author: Shell.Xu
@copyright: 2020, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import sys
import csv
import glob
import gzip
from os import path


def linefilter(src):
    for line in src:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line.replace('\t', '')


def main():
    ''' python3 cmb2csv.py [card num] [file]'''
    writer = csv.writer(sys.stdout)

    with gzip.open(sys.argv[2], 'rt', encoding='utf-8') as fi:
        for row in csv.reader(linefilter(fi)):
            if row[0] == '交易日期':
                continue
            if not row[3] or row[5] in ('信用卡存款', '信用卡还款', '受托申购', '结售汇即时售汇'):
                continue
            if row[6].startswith('转账'):
                continue
            writer.writerow([row[0][:6], row[0], sys.argv[1], row[3], row[6]])


if __name__ == '__main__':
    main()
