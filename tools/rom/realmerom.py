#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
from lxml import etree
import requests
import urllib
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

html = requests.get('https://www.realme.com/support/software-update', headers=headers).content.decode('utf-8')
hxml = etree.HTML(html)
#htree = etree.ElementTree(hxml)
softwareitems = hxml.xpath('//div[@class="software-items"]')
softwareitemlist = softwareitems[0].xpath('.//div[@class="software-item"]')

phoneinfooutf = codecs.open('realme_rom.csv', 'w', encoding='utf-8')
writer = csv.writer(phoneinfooutf)

writer.writerow(['机型','realme UI','版本','时间','大小','MD5','下载'])

for softwareitem in softwareitemlist:
    #for t in softwareitem.iter():
    #    print(t.text)
    #    print(htree.getpath(t))
    title=softwareitem.xpath('.//a[@class="software-mobile-pic"]')[0].attrib.get('title')
    print(title)
    softwareinfo=[title]
    softwaresystem=softwareitem.xpath('.//div[@class="software-system"]')[0]
    softwareinfo.append(softwaresystem.text)
    softwarefieldlist=softwareitem.xpath('.//div[@class="software-field"]')
    for softwarefield in softwarefieldlist:
        #print(etree.tostring(softwarefield))
        name=softwarefield.xpath('.//label/text()')[0]
        value=softwarefield.xpath('string(.)').strip()
        value=value[len(name):]
        if name=='版本: ':
            updatelog=softwarefield.xpath('.//a[@class="check-update-log"]/text()')[0]
            value=value[:-len(updatelog)]
        #print(name,value)
        softwareinfo.append(value)
    softwaredownload=softwareitem.xpath('.//div[@class="software-download"]/a[@class="software-button"]')[0]
    #print(softwaredownload.text,softwaredownload.attrib.get('data-href'))
    softwareinfo.append(softwaredownload.attrib.get('data-href'))
    writer.writerow(softwareinfo)

phoneinfooutf.close()
