#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2020-12-02
@author: Shell.Xu
@copyright: 2020, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
@comment:
打开招行网银个人版，切换到信用卡账单，然后从账单里用复制粘帖的方法，把文本复制到文本文件里。
文本文件放置在cmbcred/cmb-*.txt.gz。gzip压缩。数据经分析从stdout输出。
'''
import sys
import csv
import glob
import gzip
from os import path


def read_rec(fi):
    empty_line = 0
    rslt = []
    for line in fi:
        line = line.strip("￥").strip()
        if line:
            rslt.append(line)
            empty_line = 0
        elif rslt and empty_line > 12:
            if len(rslt) == 5:
                rslt.append('0.0')
            if len(rslt) == 6:
                rslt.insert(-1, 'CN')
            rslt[3] = rslt[3].replace(',', '').replace(' ', '')
            rslt[6] = rslt[6].replace(',', '').replace(' ', '')
            return rslt
        else:
            empty_line += 1
    return rslt


def main():
    writer = csv.writer(sys.stdout)
    for fn in glob.glob('cmbcred/cmb-*.txt.gz'):
        name = path.basename(fn).split('.')[0][4:]
        with gzip.open(fn, 'rt', encoding='utf-8') as fi:
            while True:
                rec = read_rec(fi)
                if not rec:
                    break
                if rec[0].startswith('12'):
                    dt = str(int(name[:4])-1)+rec[0]
                else:
                    dt = name[:4]+rec[0]
                writer.writerow([name, dt] + [rec[i] for i in (4, 3, 2)])


if __name__ == '__main__':
    main()
