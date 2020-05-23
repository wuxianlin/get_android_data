#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
import requests
import time
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
sleeptime=1

def parse_phone(writer, phone):
    phoneId = phone['id']
    phoneName = phone['name']
    print(phoneName)
    devicelist = requests.get('https://c.mi.com/oc/rom/getdevicelist?phone_id='+phoneId, headers=headers).content.decode('utf-8')
    devicelistjson = json.loads(devicelist)
    devices = devicelistjson['data']['device_data']['device_list']
    for device in devices.keys():
        roms = devices[device]
        for romtype in roms.keys():
            writer.writerow([phoneName,device,romtype,roms[romtype]['version'],roms[romtype]['rom_url'],roms[romtype]['size']])
    time.sleep(sleeptime)

if __name__ == '__main__':
    rominfooutf = codecs.open('miui_global_rom.csv', 'w', encoding='utf-8')
    writer = csv.writer(rominfooutf)
    writer.writerow(['Phone', 'Device', 'Type', 'Version', 'RomUrl', 'Size'])
    phonelist = requests.get('https://c.mi.com/oc/rom/getphonelist', headers=headers).content.decode('utf-8')
    phonelistjson = json.loads(phonelist)
    for phone in phonelistjson['data']['phone_data']['phone_list']:
        parse_phone(writer, phone)
    rominfooutf.close()
