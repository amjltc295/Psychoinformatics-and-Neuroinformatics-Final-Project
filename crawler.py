from urllib import parse,request
from bs4 import BeautifulSoup

def searchPage(link):
    URL='https://www.ptt.cc'
    URN='/ask/over18'
    q=parse.urlencode({'yes':'yes','from':link})
    q=q.encode('utf-8')
    h={'Cookie':'over18=1','User-Agent':'Mozilla/5.0'}
    req=request.Request(URL+URN,q,h) 
    data=request.urlopen(req).read()
    t=data.decode('utf-8')
    soup = BeautifulSoup(t, 'lxml')
    pushes = soup.find_all('div', 'push')
    for push in pushes:
        #state = push.find('span', 'hl push-tag').getText()
        #state2 = push.find('span', 'f1 hl push-tag').getText()
        ptt_id = push.find('span', 'f3 hl push-userid').getText()
        content = push.find('span', 'f3 push-content').getText()
        #time = push.find('span', 'push-ipdatetime').getText()
        print(ptt_id, content)

URL='https://www.ptt.cc'
URN='/ask/over18'
q=parse.urlencode({'yes':'yes','from':'/bbs/Gossiping/index23315.html'})
q=q.encode('utf-8')
h={'Cookie':'over18=1','User-Agent':'Mozilla/5.0'}
req=request.Request(URL+URN,q,h)

response=request.urlopen(req)
data=response.read()
mytext=data.decode('utf-8')

soup = BeautifulSoup(mytext, 'lxml')
articles = soup.find_all('div', 'r-ent')

NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
                         
for article in articles:
    meta = article.find('div', 'title').find('a') or NOT_EXIST
    link = meta.get('href') 
    print(link)
    searchPage(link)