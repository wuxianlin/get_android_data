#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
from selenium import webdriver
import argparse
import time

sleeptime=2

parser = argparse.ArgumentParser()
parser.description='please enter parameters region ...'
parser.add_argument('-r', '--region', help='which region you want to get rom from', dest='region', type=str, default='cn')
parser.add_argument('-o', '--output', help='output file', dest='out', type=str, default='oneplus_rom.csv')
args = parser.parse_args()

phoneinfooutf = codecs.open(args.out, 'w', encoding='utf-8')
writer = csv.writer(phoneinfooutf)

writer.writerow(['机型','类型','版本','时间','大小','MD5','下载'] if args.region=='cn' else ['Model','Build Type','Version','Updated On','Size','MD5','Download'])

# Get the Firefox profile object
profile = webdriver.firefox.webdriver.FirefoxProfile()
# Disable images
profile.set_preference('permissions.default.image', 2)
# Disable Flash
profile.set_preference(
    'dom.ipc.plugins.enabled.libflashplayer.so', 'false'
)
#profile.native_events_enabled = True
options = webdriver.firefox.options.Options()
options.headless = True
firefox = webdriver.Firefox(firefox_profile=profile, options=options, timeout=60)
firefox.get('https://www.oneplus.com/'+args.region+'/support/softwareupgrade')
try:
    firefox.find_element_by_xpath('//a[@id="close-cookie-btn"]').click()
except Exception:
    print('exception when close cookie btn')
total=0
now=0
failed=0
while now<total or total==0:
    #print(firefox.find_element_by_xpath('//*').get_attribute('outerHTML'))
    elements=firefox.find_elements_by_xpath('//div[@class="row phone-list"]/div[@class="col-sm-3 phone-item"]/div[@class="content-box"]')
    total=len(elements)
    if total==0:
        firefox.refresh()
        if failed>10:
            break
        print('failed on', now)
        failed+=1
        continue
    element=elements[now]
    time.sleep(sleeptime*2)
    element.click()
    time.sleep(sleeptime*2)
    tabs=firefox.find_elements_by_xpath('.//div[@class="support-content"]/div[@class="support-tab"]/a')
    tabnow=0
    tabnum=len(tabs)
    while tabnow<tabnum:
        time.sleep(sleeptime)
        tabs[tabnow].click()
        time.sleep(sleeptime)
        rominfo=[]
        model=firefox.find_element_by_xpath('.//div[@class="support-item active"]/div[@class="support-version"]/div[@class="banner-img"]/div[@class="upgrade"]/p[@class="name"]').text
        print(model)
        rominfo.append(model)
        rominfo.append(tabs[tabnow].text)
        infos=firefox.find_elements_by_xpath('.//div[@class="support-item active"]/div[@class="support-version"]/div[@class="banner-desc"]/div[@class="info"]')
        for info in infos:
            #print(info.find_element_by_xpath('.//h4').text)
            rominfo.append(info.find_element_by_xpath('.//p').text)
        download=firefox.find_element_by_xpath('.//div[@class="support-item active"]/div[@class="support-version"]/div[@class="banner-desc"]/a[@href]')
        rominfo.append(download.get_attribute('href'))
        writer.writerow(rominfo)
        tabnow+=1
    now+=1
    time.sleep(sleeptime)
    firefox.back()
    time.sleep(sleeptime)
firefox.close()
firefox.quit()
phoneinfooutf.close()

if failed>10:
    raise Exception('timeout')

