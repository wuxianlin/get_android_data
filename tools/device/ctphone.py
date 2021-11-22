#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import argparse
import codecs
import csv
from lxml import etree
import requests
import re
import time
import urllib
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
sleeptime=5

parser = argparse.ArgumentParser()
parser.description='please enter parameters ...'
parser.add_argument('-k', '--keyword', help='which keyword you want to get phone from', dest='keyword', type=str, default='OPPO')
parser.add_argument('-o', '--output', help='output file', dest='out', type=str, default='oppo_phone.csv')
args = parser.parse_args()

html = requests.get('http://surfing.tydevice.com/pud_phone_list.do?protype=mobile&pid=10000&keyword='+args.keyword+'&pageSize=1000&selectPage=1', headers=headers).content.decode('utf-8')
hxml = etree.HTML(html)
divs = hxml.xpath('//div[@class="propic"]')

phoneinfooutf = codecs.open(args.out, 'w', encoding='utf-8')
writer = csv.writer(phoneinfooutf)

wants= ['宣传名称','品牌','产品型号','产品上市时间','产品零售价格','屏幕尺寸','AP型号','智能操作系统']

writer.writerow(wants)

for div in divs:
    a = div.xpath('.//a')
    href = a[0].attrib.get('href')
    onclick = a[0].attrib.get('onclick')
    onclicksplit = re.split('[,\']',onclick)
    #print(a[0].attrib.get('href'))
    print(a[0].attrib.get('onclick'))

    #href='prodetail.do?pro_id=93010&navId=nav_cpk'
    #onclick='setProHistory(\'93010,OPPO,PCLM10\')'

    datas = {}

    result = urllib.parse.urlparse(href)
    pro_id = urllib.parse.parse_qs(result.query,True)['pro_id'][0]
    if pro_id is None or pro_id.strip()=='':
        pro_id = onclicksplit[1]
    time.sleep(sleeptime)
    tag = requests.get('http://surfing.tydevice.com/prochangetag.do?pro_id=' + pro_id + '&attrCode=660010000', headers=headers)
    tagjson = json.loads(tag.text)
    #print(tagjson)
    if tagjson['list'] != 'null':
        for taglist in tagjson['list']:
            datas[taglist['attr_name']]=taglist['pro_attr_values']
            #print(taglist['attr_name'], taglist['pro_attr_values'])
    #for tagversion in tagjson['version']:
        #datas[tagversion['attr_name']]=tagversion['pro_attr_values']
        #print(tagversion['attr_name'], tagversion['pro_attr_values'])

    time.sleep(sleeptime)
    detailhtml = requests.get('http://surfing.tydevice.com/' + href, headers=headers).content.decode('utf-8')
    detailhxml = etree.HTML(detailhtml)
    tables = detailhxml.xpath('//div[@class="show_t"]')[0].xpath('.//table')
    for table in tables:
        trs = table.xpath('.//tr')
        for tr in trs:
            tds = tr.xpath('.//td')
            if len(tds)==2:
                key = tds[0].text
                datas[key if key is None else key.replace('：', '')] = tds[1].text.strip()
            #for td in tds:
            #    print(td.text)

    #print(datas)
    wanted = []
    for want in wants:
        if want in datas.keys():
            wanted.append(datas[want])
        elif want == '品牌':
            wanted.append(onclicksplit[2])
        elif want == '产品型号':
            wanted.append(onclicksplit[3])
        else:
            wanted.append('N/A')
    writer.writerow(wanted)

phoneinfooutf.close()
