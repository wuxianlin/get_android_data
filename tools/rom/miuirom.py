#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
from lxml import etree
import re
import requests
import time
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
sleeptime=1

def parse_phone(writer, phone):
    phoneId = phone['pid']
    phoneName = phone['name']
    print(phoneName)
    devicelist = requests.get('https://www.miui.com/download-'+phoneId+'.html', headers=headers).content.decode('utf-8')
    hxml = etree.HTML(devicelist)
    deviceinfo={}
    for device in hxml.xpath('//span[@class="tab"]'):
        deviceinfo[device.attrib.get('id')]=device.text
    for div in hxml.xpath('//div[@class="content"]|//div[@class="content current_content"]'):
        device=phoneName
        if div.attrib.get('class')=='content':
            key=div.attrib.get('id')[len('content_'):]
            if key in deviceinfo.keys():
                device=deviceinfo[key]
        romtype=''
        version=''
        size=''
        url=''
        for rominfo in div.xpath('.//h2|.//p|.//a[@class="download_btn"]'):
            if rominfo.tag == 'h2':
                romtype=rominfo.text
            elif rominfo.tag == 'p':
                value=rominfo.xpath('string(.)').strip()
                matchObj = re.search( r'版本：(.*)\n大小：(.*)', value, re.M|re.I)
                if matchObj:
                    version=matchObj.group(1)
                    size=matchObj.group(2)
            elif rominfo.tag == 'a':
                url=rominfo.attrib.get('href')
            if not romtype == '' and not version == '' and not size == '' and not url == '':
                writer.writerow([phoneName,device,romtype,version,url,size])
                romtype=''
                version=''
                size=''
                url=''
    time.sleep(sleeptime)

if __name__ == '__main__':
    rominfooutf = codecs.open('miui_rom.csv', 'w', encoding='utf-8')
    writer = csv.writer(rominfooutf)
    writer.writerow(['系列', '机型', '类型', '版本', '地址', '大小'])
    phonelist = requests.get('https://www.miui.com/download.html', headers=headers).content.decode('utf-8')
    matchObj = re.search( r'phones =(.*?);', phonelist, re.M|re.I)
    if matchObj:
        phonelistjson = json.loads(matchObj.group(1))
        phonelistjson.sort(key = lambda x:x['pid'])
        for phone in reversed(phonelistjson):
            parse_phone(writer, phone)
    rominfooutf.close()
