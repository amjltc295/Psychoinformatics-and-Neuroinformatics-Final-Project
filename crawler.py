import requests
from bs4 import BeautifulSoup
import time
from dataIO import TypeResultWrapper, WordResultWrapper

def getPageText(link):
    pageText=requests.get(link, cookies={'over18':'1'}).text
    return pageText

def getTitle(soup):
    return soup.find('span', 'article-meta-value').getText()

def getContent_pushes(soup):
    s=soup.find_all('span', 'f6')
    for i in s:
        i.decompose()
    content = soup.find(id="main-content").text
    target_front = u'時間'
    target_back = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
    content = content.split(target_back)
    content = content[0].split(target_front)
    main_content = content[1]
    return main_content

# search an article page
def searchPage(link,keyWord):
    ww=WordResultWrapper(keyWord)
    t = getPageText(link)
    soup = BeautifulSoup(t, 'lxml')
    #title
    title = getTitle(soup)
    ww.titleNum = searchKeyword(title,keyWord)
    #content
    content = getContent_pushes(soup)
    ww.contentNum = searchKeyword(content,keyWord)
    #pushes
    pushes = soup.find_all('div', 'push')
    for push in pushes:
        #state = push.find('span', 'hl push-tag').getText()
        #state2 = push.find('span', 'f1 hl push-tag').getText()
        #ptt_id = push.find('span', 'f3 hl push-userid').getText()
        comment = push.find('span', 'f3 push-content').getText()
        #print(comment)
        ww.commentNum += searchKeyword(comment,keyWord)
    print(ww.titleNum, ww.contentNum, ww.commentNum)
    #ww.printWordResult
    return ww

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
N=1
'''
f = open("test.txt","w") #opens file with name of "test.txt"
prevPage='https://www.ptt.cc/bbs/Gossiping/index'+pageNum+'.html'
pageText = getPageText(prevPage)
soup = BeautifulSoup(pageText, 'lxml')
f.write(soup.text)
print(soup.text)
f.close()

'''
for i in range(N): # 翻頁N次
    prevPage='https://www.ptt.cc/bbs/Gossiping/index'+pageNum+'.html'
    print('page', pageNum)
    pageText = getPageText(prevPage)

    soup = BeautifulSoup(pageText, 'lxml')
    articles = soup.find_all('div', 'r-ent')

    NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
                             
    for article in articles:
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        if(meta != NOT_EXIST):
            link = meta.get('href') 
            print(link)        #印文章連結
            searchPage('https://www.ptt.cc'+link,u'我')
    #next page
    pageNum=getPrevPage(soup)
   
end = time.time()
print('time:', end - start, 'seconds')
input('Done')