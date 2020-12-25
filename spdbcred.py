#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2020-12-07
@author: Shell.Xu
@copyright: 2020, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
@comment:
依赖xlrd
从浦发个人网银进入信用卡账单页面，选择某个月下载，输出文件名为"xxx年月日交易明细表.xls"。
将文件放在spdbcred路径下，执行脚本。数据从stdout中输出。
'''
import re
import sys
import csv
import glob

import xlrd


re_month = re.compile(r'\D+(\d+)\D+')


def main():
    writer = csv.writer(sys.stdout)

    for fn in glob.glob('spdbcred/*交易明细报表.xls'):
        m = re_month.match(fn)
        name = m.groups()[0]

        xl_workbook = xlrd.open_workbook(fn)
        xl_sheet = xl_workbook.sheet_by_name('账单明细')
        for row_idx in range(1, xl_sheet.nrows):
            row = xl_sheet.row(row_idx)
            if '转账还款' in row[2].value:
                continue
            writer.writerow([name,] + [row[i].value for i in (0, 3, 6, 2)])


if __name__ == '__main__':
    main()
