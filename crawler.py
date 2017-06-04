from urllib import parse,request
from bs4 import BeautifulSoup

# get text of an index page
def getPageText(req):
    response=request.urlopen(req)
    data=response.read()
    mytext=data.decode('utf-8')
    return mytext

# search all pushes in an article page
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
        print(ptt_id, content)

# get the number of previous page
def getPrevPage(text): 
    soup = BeautifulSoup(text, 'lxml')
    prevPage = str(soup.find_all('a', 'btn wide')[1])
    x=str(prevPage).find('index')
    y=str(prevPage).find('.html')
    return prevPage[x+5:y]

URL='https://www.ptt.cc'
URN='/ask/over18'
h={'Cookie':'over18=1','User-Agent':'Mozilla/5.0'}

pageNum=''

for i in range(5): # 翻頁5次
    prevPage='/bbs/Gossiping/index'+pageNum+'.html'
    print(prevPage) #印index網址
    q=parse.urlencode({'yes':'yes','from':prevPage}).encode('utf-8')
    req=request.Request(URL+URN,q,h)
    pageText=getPageText(req) #Page 1

    soup = BeautifulSoup(pageText, 'lxml')
    articles = soup.find_all('div', 'r-ent')

    NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
                             
    for article in articles:
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        link = meta.get('href') 
        #print(link)        #印文章連結
        #searchPage(link)   #印推文

    #next page
    pageNum=getPrevPage(pageText)
    
    

input('Done')