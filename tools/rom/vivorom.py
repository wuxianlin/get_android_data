#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
from lxml import etree
import requests
import time
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
sleeptime=1

if __name__ == '__main__':
    rominfooutf = codecs.open('vivo_rom.csv', 'w', encoding='utf-8')
    writer = csv.writer(rominfooutf)
    writer.writerow(['系列', '机型', '地址', '大小', '时间'])
    brandlist = requests.get('https://www.vivo.com.cn/upgrade/getModels', headers=headers).content.decode('utf-8')
    brandlistjson = json.loads(brandlist, strict=False)
    for brand in brandlistjson['data']:
        brandName=brand['seriesName']
        for product in brand['products']:
            productName=product['name']
            print(productName)
            productId=product['id']
            html = requests.get('https://www.vivo.com.cn/upgrade/detail?modelId='+str(productId), headers=headers).content.decode('utf-8')
            hxml = etree.HTML(html)
            url=''
            date=''
            size=''
            for packinfo in hxml.xpath('//div[@class="pack-info"]/*'):
                if packinfo.tag == 'a':
                    url=packinfo.attrib.get('href')
                elif packinfo.text.startswith('更新时间: '):
                    date=packinfo.text[5:].strip()
                elif packinfo.text.startswith('文件大小: '):
                    size=packinfo.text[5:].strip()
            writer.writerow([brandName,productName,url,size,date])
            time.sleep(sleeptime)
    rominfooutf.close()
