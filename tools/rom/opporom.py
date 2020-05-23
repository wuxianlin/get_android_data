#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
import requests
import time
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
sleeptime=2

def parse_brand(writer, brand):
    brandId = brand['brandId']
    brandName = brand['brandName']
    productList = requests.get('https://bbs.coloros.net/V1/product/getProductList?brandId='+brandId, headers=headers).content.decode('utf-8')
    productlistjson = json.loads(productList)
    for product in productlistjson['data']:
        parse_product(writer, brandName, product)
    time.sleep(sleeptime)

def parse_product(writer, brandName, product):
    productId = product['productId']
    productName = product['productName']
    print(productName)
    romInfo = requests.get('https://bbs.coloros.net/V1/oppoRom/getRomInfo?productId='+productId, headers=headers).content.decode('utf-8')
    romInfojson = json.loads(romInfo)
    parse_rom(writer, brandName, productName, romInfojson['data'])
    time.sleep(sleeptime*2)

def parse_rom(writer, brandName, productName, romList):
    writer.writerow([brandName, productName, romList['romName'], romList['romVersion'], romList['colorVersion'], romList['androidVersion'], romList['fileUrl'], romList['fileSizeAlias'], romList['releasePackageDate'], romList['md5']])
    if not romList['oppoRomList'] is None:
        for rom in romList['oppoRomList']:
            parse_rom(writer, brandName, productName, rom)

if __name__ == '__main__':
    rominfooutf = codecs.open('oppo_rom.csv', 'w', encoding='utf-8')
    writer = csv.writer(rominfooutf)
    writer.writerow(['系列', '机型', '名称', '版本', 'ColorOS', 'Android', '地址', '大小', '时间', 'MD5'])
    brandlist = requests.get('https://bbs.coloros.net/V1/oppoBrand/getBrandList', headers=headers).content.decode('utf-8')
    brandlistjson = json.loads(brandlist)
    for brand in brandlistjson['data']:
        parse_brand(writer, brand)
    rominfooutf.close()
