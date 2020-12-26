#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2020-12-08
@author: Shell.Xu
@copyright: 2020, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import sys
import csv
import json
import pprint


def main():
    writer = csv.writer(sys.stdout)
    writer.writerow(('orderid', 'date', 'name', 'type', 'cost'))

    with open('jd-type.csv') as fi:
        types = {row[5]: row[6] for row in csv.reader(fi) if row[5]}

    with open('jd-order.csv') as fi:
        for row in csv.reader(fi):
            if row[1] == 'web-scraper-start-url':
                continue
            if not row[2] or row[2] == 'null':
                continue
            objs = json.loads(row[3])
            href = objs[0]['name-href']
            if href.startswith('//'):
                href = 'https:'+href
            ordertype = types.get(href, 'unknown')
            writer.writerow((row[5], row[6], objs[0]['name'], ordertype, row[2].strip('¥')))


if __name__ == '__main__':
    main()
