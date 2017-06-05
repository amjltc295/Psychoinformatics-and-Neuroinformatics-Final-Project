import requests
from bs4 import BeautifulSoup
import time

# get text of an index page
def getPageText(link):
    pageText=requests.get(link, cookies={'over18':'1'}).text
    return pageText

# search all pushes in an article page
def searchPage(link,keyWord):
    count=0
    t = getPageText(link)
    soup = BeautifulSoup(t, 'lxml')
    pushes = soup.find_all('div', 'push')
    for push in pushes:
        #state = push.find('span', 'hl push-tag').getText()
        #state2 = push.find('span', 'f1 hl push-tag').getText()
        #ptt_id = push.find('span', 'f3 hl push-userid').getText()
        content = push.find('span', 'f3 push-content').getText()
        print(content)
        count += searchKeyword(content,keyWord)
    return count

# get the number of previous page
def getPrevPage(soup): 
    prevPage = str(soup.find_all('a', 'btn wide')[1])
    x=str(prevPage).find('index')
    y=str(prevPage).find('.html')
    return prevPage[x+5:y]

def searchKeyword(text,word):
    count=0
    a=0
    while(a>=0):
        a=text.find(word)
        if(a>=0):
            count+=1
            text=text[a+len(word):]
    return count

start = time.time()

pageNum=''
count=0
N=2
for i in range(N): # 翻頁N次
    prevPage='https://www.ptt.cc/bbs/Gossiping/index'+pageNum+'.html'
    #print(prevPage)
    pageText = getPageText(prevPage)

    soup = BeautifulSoup(pageText, 'lxml')
    articles = soup.find_all('div', 'r-ent')

    NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
                             
    for article in articles:
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        link = meta.get('href') 
        print(link)        #印文章連結
        count += searchPage('https://www.ptt.cc'+link,'我')   
        print(count)
    #next page
    pageNum=getPrevPage(soup)
    
end = time.time()
print('time:', end - start)
input('Done')