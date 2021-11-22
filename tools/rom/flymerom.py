#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
from selenium import webdriver
import requests
import time
import urllib
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
sleeptime = 1

phoneinfooutf = codecs.open('flyme_rom.csv', 'w', encoding='utf-8')
writer = csv.writer(phoneinfooutf)

writer.writerow(['机型','网络','类型','版本','MD5','下载','大小','时间'])

# Get the Firefox profile object
#profile = webdriver.firefox.webdriver.FirefoxProfile()
# Disable images
#profile.set_preference('permissions.default.image', 2)
# Disable Flash
#profile.set_preference(
#    'dom.ipc.plugins.enabled.libflashplayer.so', 'false'
#)
#profile.native_events_enabled = True
options = webdriver.firefox.options.Options()
options.headless = True
#options.profile = profile
firefox = webdriver.Firefox(options=options, timeout=60)
firefox.get('https://www.flyme.cn/firmware.html')

total=0
now=0
failed=0
while now<total or total==0:
    devices = firefox.find_elements_by_xpath('//ul[@id="all_brand_content_3"]/li/a[@href]')
    total=len(devices)
    if total==0:
        firefox.refresh()
        if failed>10:
            break
        print('failed on', now)
        failed+=1
        continue
    device=devices[now]
    link=device.get_attribute('href')
    model=device.get_attribute('title')
    print(model)
    nettype=''
    romtype=''
    time.sleep(sleeptime*2)
    firefox.get(link)
    time.sleep(sleeptime*2)
    version=''
    url=''
    md5=''
    size=''
    date=''
    nettabs=firefox.find_elements_by_xpath(".//ul[@id='net_box']/li")
    for nettab in nettabs:
        nettype=nettab.text
        nettab.click()
        basetabs=firefox.find_elements_by_xpath(".//ul[@id='base_box']/li")
        for basetab in basetabs:
            romtype=basetab.text.replace('\n',' ').replace('\r',' ')
            basetab.click()
            for info in firefox.find_elements_by_xpath('//div/a[@class="info_down"]|//ul[@class="info_base"]/li'):
                if info.tag_name == 'a':
                    url=info.get_attribute('href')
                    if url.endswith('#'):
                       info.click()
                       url=firefox.find_element_by_xpath('//div/a[@class="confirm"]').get_attribute('href')
                       firefox.find_element_by_xpath('//div/a[@class="choose"]').click()
                elif info.tag_name == 'li':
                    if info.text.startswith('版本：'):
                        version=info.text[3:]
                    elif info.text.startswith('MD5：'):
                        md5=info.text[4:]
                    elif info.text.startswith('文件大小：'):
                        size=info.text[5:]
                    elif info.text.startswith('发布时间：'):
                        date=info.text[5:]
            writer.writerow([model,nettype,romtype,version,md5,url,size,date])
            div = firefox.find_element_by_xpath('//div[@class="firm_table"]')
            if 'none' in div.get_attribute('style'):
                continue
            for tr in div.find_elements_by_xpath('.//table/tbody[@id="history"]/tr'):
                tds=tr.find_elements_by_xpath('.//td')
                if len(tds) == 6:
                    version=tds[0].text
                    size=tds[1].text
                    md5=tds[2].text[4:]
                    date=tds[5].text
                    url=tds[4].find_element_by_xpath('.//a[@href]').get_attribute('href')
                    writer.writerow([model,nettype,romtype,version,md5,url,size,date])
    now+=1
    time.sleep(sleeptime)
    firefox.back()
    time.sleep(sleeptime)

firefox.close()
firefox.quit()

phoneinfooutf.close()

if failed>10:
    raise Exception('timeout')
