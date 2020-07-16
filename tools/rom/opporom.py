#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
import requests
import time
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
sleeptime=5

def parse_brand(writer, brand):
    brandId = brand['id']
    brandName = brand['brandName']
    productList = requests.get('https://www.coloros.com/api/colorOS/business/rom/productList?brandId='+str(brandId), headers=headers).content.decode('utf-8')
    productlistjson = json.loads(productList)
    for product in productlistjson['data']:
        parse_product(writer, brandName, product)
    time.sleep(sleeptime)

def parse_product(writer, brandName, product):
    productId = product['id']
    productName = product['productName']
    print(productName)
    romInfo = requests.get('https://www.coloros.com/api/colorOS/business/rom/romList?productId='+productId, headers=headers).content.decode('utf-8')
    romInfojson = json.loads(romInfo)
    for rom in romInfojson['data']:
        writer.writerow([brandName, productName, rom['version'], rom['colorosVersion'], rom['androidVersion'], rom['fileUrl'], rom['fileSize'], rom['updateTime'], rom['fileMd5']])
    time.sleep(sleeptime*2)

if __name__ == '__main__':
    rominfooutf = codecs.open('oppo_rom.csv', 'w', encoding='utf-8')
    writer = csv.writer(rominfooutf)
    writer.writerow(['系列', '机型', '版本', 'ColorOS', 'Android', '地址', '大小', '时间', 'MD5'])
    brandlist = requests.get('https://www.coloros.com/api/colorOS/business/rom/brandList', headers=headers).content.decode('utf-8')
    brandlistjson = json.loads(brandlist)
    for brand in brandlistjson['data']:
        parse_brand(writer, brand)
    rominfooutf.close()
