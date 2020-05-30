#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
from lxml import etree
import argparse
import requests
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

parser = argparse.ArgumentParser()
parser.description='please enter parameters ...'
parser.add_argument('-t', '--type', help='images or ota', dest='type', type=str, default='images')
parser.add_argument('-o', '--output', help='output file', dest='out', type=str, default='android_images.csv')
args = parser.parse_args()

#domain='https://developers.google.com'
domain='https://developers.google.cn'
html = requests.get(domain+'/android/'+args.type, headers=headers).content.decode('utf-8')
hxml = etree.HTML(html)
cveoutf = codecs.open(args.out, 'w', encoding='utf-8')
writer = csv.writer(cveoutf)
writer.writerow(['Model','Version','Download','SHA-256 Checksum'])

roms=[]
model=''
for t in hxml.xpath('//h2[@data-text]|//table'):
    if t.tag == 'h2':
        model=t.attrib.get('data-text')
    elif t.tag == 'table':
        title=[]
        for th in t.xpath('.//th'):
            title.append(th.text)
        for tr in t.xpath('.//tr'):
            content=[]
            content.append(model)
            for trtd in tr.xpath('.//td'):
                td=trtd.text.strip() if trtd.text is not None else ''
                for tra in trtd.xpath('.//a[@href]'):
                    td+=('' if td =='' else ' ')+tra.attrib.get('href')
                content.append(td)
            writer.writerow(content)
cveoutf.close()
