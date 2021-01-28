#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2020-12-02
@author: Shell.Xu
@copyright: 2020, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
@comment:
进入招行大众版，选择查看流水并导出，选择csv格式。将结果用gzip压缩后存放。
执行脚本时，第一个参数跟csv文件。
stdout会输出所有消费。
'''
import sys
import csv
import glob
import gzip
from os import path


cardnum = None


def linefilter(src):
    for line in src:
        line = line.strip()
        if line.startswith('# 账'):
            global cardnum
            cardnum = line.split('********')[1][:4]
        if not line or line.startswith('#'):
            continue
        yield line.replace('\t', '')


# 信用卡存款, 信用卡还款
# 朝朝宝转入, 朝朝宝转出
# 黄金交易
# 债券买卖
# 受托申购-买理财, 受托分红-分红, 备注格式-产品ID,日期/流水号
# 基金申购-买基金, 备注格式-基金ID
# 结售汇即时售汇-换外汇
# 国际结算费用-国际汇费
# 转账汇款-汇款, 行内汇入-本行汇入, 客户转账-外行转账
# U1PY/N5CP-财付通-微信支付
# 线上支付-闪付
non_types = {
    '信用卡存款', '信用卡还款', '朝朝宝转入', '黄金交易', '债券买卖',
    '受托申购', '基金申购', '结售汇即时售汇'}

def main():
    ''' python3 cmb2csv.py [file]'''
    writer = csv.writer(sys.stdout)

    with gzip.open(sys.argv[1], 'rt', encoding='gbk') as fi:
        for row in csv.reader(linefilter(fi)):
            if row[0] == '交易日期':
                continue
            if not row[3] or row[5] in non_types:
                continue
            # "转账汇款"或"客户转账"类别的支出，有时备注没有目标名称
            # 只有"转账"二字，这种都是转给自己的
            # 有时是"转账"+自己的名字
            # 这两种统一处理
            if row[5] in {'转账汇款', '客户转账'} and row[6].startswith('转账'):
                continue
            writer.writerow([row[0][:6], row[0], cardnum, row[3], row[6]])


if __name__ == '__main__':
    main()
