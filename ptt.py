# -*- coding: utf-8 -*-
"""
Psychoinfomatics and Neuroinformatics
HW4
NTUEE3 B03901014 Ya-Liang Chang
"""
import urllib.request, lxml.html
from selenium import webdriver

print ("NTUEE3 B03901014 Ya-Liang Chang")
print (" ")
"""
HW4-1
Get the total number of history page of specified website,
using LXML.
"""
u='http://www.ptt.cc/bbs/Boy-Girl/'
h={'User-Agent':'Mozilla/5.0'}
r=urllib.request.Request(u,headers=h)
data=urllib.request.urlopen(r).read()
t=lxml.html.fromstring(data.decode('utf-8'))
#for link in t.xpath('//a'):
#    print(link.text,link.attrib.get('href'))
#print(t.text_content())
page_num = 0
titles = [] #titles of 爆 and related info
for link in t.xpath('//a'):
    #print(link.text,link.attrib.get('href'))
    #if (str(link.text).find('上頁') != -1):
    if ('上頁' in str(link.text)):
        #print (link.attrib.get('href'))
        link_txt = str(link.attrib.get('href'))
        index = link_txt.find('index') + 5
        if (index != -1):
            page_num = link_txt[index:].split('.')[0]
print ("HW4-1")
print ("Total number of page in Boy-Gril: ", page_num)
print (' ')

"""
HW4-2
Get the title and URN of article with popularity index "爆",
using LXML.
"""
for span in t.xpath('//span'):
    class_name = str( span.attrib.get('class') )
    #Note: need to exclude '爆' in the title
    if (class_name  == 'hl f1' and '爆' in str(span.text)):# or class_name == 'hl f2' or class_name == 'hl f3'):
        #print (span.text)
        parent = span.getparent().getparent()#.getnext().getchildren()
        for each in parent:
            #print (each.attrib)
            if ('title' in each.attrib.get('class') and each.getchildren()):
                this_title = each.getchildren()[0]
                titles.append([span.text, this_title.text, this_title.attrib.get('href')]) #[reply_num, title, url]

print ('HW4-2')
for each_title in titles:
    print (each_title[0], '\t',  each_title[1], '\t', each_title[2])
print (' ')
"""
HW4-3
Use selenium to go to last three page and take a picture.
"""
print ('HW4-3')
driver = webdriver.Chrome() # or webdriver.Firefox()
URL = 'http://www.ptt.cc/bbs/Boy-Girl/'
driver.get(URL)
driver.save_screenshot('before_click.png')
print ('before_click.png saved')
for i in range(3):
    #button = driver.find_element_by_name('< 上頁')
    button = driver.find_elements_by_xpath("//*[contains(text(), '上頁')]")[0]
    button.click()
driver.save_screenshot('after_click.png')
print ('after_click.png saved')

"""
x=t.xpath('//div[@id="main-container"]')[0]
print(x.text_content()) # 主文
y=t.xpath('//div[@id="main-container"]/text()')
print (y)
print(''.join(y)) # 新文
z=t.xpath('//span[@class="f6"]')
for i in z:
    print(i.text) # 引言
    H=t.xpath('//*[contains(text()," 恨 ")]')[0]
    print(H.text) # 含恨
"""
