# -*- coding: utf-8 -*-
"""
Psychoinfomatics and Neuroinformatics
HW5
NTUEE3 B03901014 Ya-Liang Chang
"""
import urllib.request,json

print ("NTUEE3 B03901014 Ya-Liang Chang")
print (" ")
"""
HW5-1
Modify the program to get pictures from articles with tag "女友".
"""
from dcard import Dcard
def hot(metas):
    #return [m for m in metas if m['likeCount'] >= 100]
    return [m for m in metas if "女友" in m['tags']]
d=Dcard()
f=d.forums('photography') # 攝影版
m=f.get_metas(num=50,callback=hot) #list
print ("#########")
print ("# HW5-1 #")
print ("#########")
print (' ')
print ("Posts with tags '女友' in the latest 50: ")
for eachPost in m:
    print ('\t', eachPost['id'], eachPost['title'], eachPost['tags'])
p=d.posts(m).get(comments=False,links=False)
r=p.parse_resources() #list: try r[0][1]
done,fails=p.download(r)

print('Got %d pics' % done if len(fails)==0 else 'Error!')
print (' ')
print (' ')

