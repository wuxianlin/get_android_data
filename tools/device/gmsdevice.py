#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import argparse
import codecs
import csv
from lxml import etree
import requests
import urllib
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

parser = argparse.ArgumentParser()
parser.description='please enter parameters ...'
parser.add_argument('-b', '--brand', help='which brands you want to get phone from', dest='brand', type=str, default='OnePlus,Oppo,Realme')
parser.add_argument('-o', '--output', help='output file', dest='out', type=str, default='oplus_gms_devices.csv')
args = parser.parse_args()

phoneinfooutf = codecs.open(args.out, 'w', encoding='utf-8')
writer = csv.writer(phoneinfooutf)

#https://support.google.com/googleplay/answer/1727131?hl=en
html = requests.get('https://storage.googleapis.com/play_public/supported_devices.html', headers=headers).content.decode('utf-8')
hxml = etree.HTML(html)
trs = hxml.xpath('//table/tr')

for tr in trs:
    tds = tr.xpath('.//td')
    if len(tds)>0:
        content=[]
        for td in tds:
            content.append(td.text)
        if len(content)>0 and content[0] is not None and content[0] in args.brand.split(","):
            print(content)
            writer.writerow(content)
    else:
        ths = tr.xpath('.//th')
        if len(ths)>0:
            titles=[]
            for th in ths:
                titles.append(th.text)
            print(titles)
            writer.writerow(titles)

phoneinfooutf.close()
