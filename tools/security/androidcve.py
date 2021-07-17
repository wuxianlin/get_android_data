#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'wuxianlin'

import codecs
import csv
from lxml import etree
import requests
import json

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

#domain='https://source.android.com'
domain='https://source.android.google.cn'
links = []
for url in ['/security/bulletin?hl=en',  '/security/bulletin/pixel?hl=en']:
    html = requests.get(domain+url, headers=headers).content.decode('utf-8')
    hxml = etree.HTML(html)
    links += hxml.xpath('//tr/td[1]/a[@href]')

cveoutf = codecs.open('cve.csv', 'w', encoding='utf-8')
writer = csv.writer(cveoutf)
writer.writerow(['cve','securitypatchlevel','reference','type','severity','aospversion','securitycomponent','component','other'])

cves=[]

for link in links:
    href=link.attrib.get('href')
    print(href)
    #continue
    detailhtml = requests.get(domain+href+'?hl=en', headers=headers).content.decode('utf-8')
    detailhxml = etree.HTML(detailhtml)
    detailsdate = ''
    component = ''
    for t in detailhxml.xpath('//h2[@id]|//h3[@id]|//table'):
        if t.tag == 'h2' :
            h2id=t.attrib.get('id')
            #print(h2id)
            if h2id.endswith('-security-patch-level—vulnerability-details'):
                detailsdate=h2id[:-len('-security-patch-level—vulnerability-details')]
            elif h2id.endswith('-security-patch-level-vulnerability-details'):
                detailsdate=h2id[:-len('-security-patch-level-vulnerability-details')]
            elif h2id.endswith('-spl-details'):
                detailsdate=h2id[:-len('-spl-details')]
            elif h2id.endswith('-details'):
                detailsdate=h2id[:-len('-details')]
                if len(detailsdate)<10:
                    detailsdate=t.attrib.get('data-text').split(' ')[0]
            elif h2id.startswith('details-') or h2id.startswith('detsild-'):
                detailsdate=href[href.rfind('/')+1:href.rfind('-')+1]+h2id[len('details-'):]
            elif h2id == 'vulnerability details' and 'android-10' in href:
                detailsdate='2019-09-01'
            elif h2id.endswith('spl'):
                detailsdate=href[href.rfind('/')+1:href.rfind('-')+1]+h2id[:-len('spl')]
            elif ('2015' in href or '2016' in href) and ('_details' in h2id or ('2015-08-01' in href and 'acknowledgements' in h2id)):
                detailsdate=href[href.rfind('/')+1:]
            elif 'patches' in h2id and 'functional' not in h2id and 'pixel' in href:
                detailsdate=href[href.rfind('/')+1:]
            else :
                print(h2id)
                detailsdate = ''
                component = ''
                continue
        elif not detailsdate == '' and t.tag == 'h3' :
            h3id=t.attrib.get('id')
            #print(h3id)
            component=h3id
        elif not detailsdate == '' and not component == '':
            title=[]
            for th in t.xpath('.//th'):
            	if th.text:
                    title.append(th.text.strip())
            rowspans={}
            for tr in t.xpath('.//tr'):
                content=[]
                nowrow=0
                for trtd in tr.xpath('.//td'):
                    while nowrow in rowspans.keys():
                        rowspan=rowspans[nowrow]
                        if rowspan['size']>0:
                            content.append(rowspan['content'])
                            rowspan['size']-=1
                            nowrow+=1
                        else:
                            break
                    #content.append(trtd.xpath('string(.)').strip())
                    td=trtd.text.strip() if trtd.text is not None else ''
                    for tra in trtd.xpath('.//a[@href]'):
                        td+=('' if td =='' else ' ')+'['+tra.text.strip()+']('+tra.attrib.get('href')+')'
                    if 'rowspan' in trtd.attrib.keys():
                        rowspan={}
                        rowspan['size']=int(trtd.attrib.get('rowspan'))-1
                        rowspan['content']=td
                        rowspans[nowrow]=rowspan
                    nowrow+=1
                    content.append(td.replace('\n',' ').replace('\r',' '))
                    while nowrow in rowspans.keys():
                        rowspan=rowspans[nowrow]
                        if rowspan['size']>0:
                            content.append(rowspan['content'])
                            rowspan['size']-=1
                            nowrow+=1
                        else:
                            break
                if len(content)>0 and len(title)==len(content):
                    cve=dict(zip(title,content))
                    cve['SecurityPatchLevel']=detailsdate
                    cve['SecurityComponent']=component
                    if 'android-10' in href:
                        cve['Updated AOSP versions']='10'
                    cves.append(cve)
                    #print(cve)
    #print(cves)
    #break

#print(cves)
for cve in cves:
    cveid='N/A'
    securitypatchlevel='N/A'
    reference='N/A'
    securitytype='N/A'
    severity='N/A'
    aospversion='N/A'
    securitycomponent='N/A'
    component='N/A'
    other=''
    for key in cve.keys():
        if key in ['CVE','CVEs']:
            cveid=cve[key]
        elif key == 'SecurityPatchLevel':
            securitypatchlevel=cve[key]
        elif key in ['References','Bugs','Bug','Bug(s)','Bugs with AOSP links','Bug with AOSP link','Bug with AOSP links','Bugs with AOSP link','Bug(s) with AOSP Link','Bug(s) with AOSP link','Bug(s) with AOSP links','Android bugs','Android bug']:
            reference=cve[key]
        elif key == 'Type':
            securitytype=cve[key]
        elif key in ['Severity','Severity*']:
            severity=cve[key]
        elif key in ['Updated AOSP versions','Affected versions','Affected Versions','Updated versions']:
            aospversion=cve[key]
        elif key == 'SecurityComponent':
            securitycomponent=cve[key]
        elif key == 'Component':
            component=cve[key]
        elif cve[key] is not None:
            other+=('' if other=='' else ' ')+key+'='+cve[key]
    writer.writerow([cveid,securitypatchlevel,reference,securitytype,severity,aospversion,securitycomponent,component,other])
  
cveoutf.close()
