import requests
from multiprocessing import Process
from bs4 import BeautifulSoup
import time
from dataIO import TypeResultWrapper, WordResultWrapper
import sys, os

def getPageText(link):    
    #a = time.time()
    if(link == 'empty'):
        pageText='This page has been deleted.'
    else:
        pageText=requests.get(link, cookies={'over18':'1'}).text
    #b = time.time()
    #print('get page text time:', b-a)
    return pageText

def getTitle(soup):
    return soup.find('span', 'article-meta-value').getText()

def getContent(soup):
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
    t = getPageText(link)
    return searchText(t)

# search from file
def searchText(text,keyWord):
    #a = time.time()
    ww = WordResultWrapper(keyWord)
    soup = BeautifulSoup(text, 'lxml')
    #title
    title = getTitle(soup)
    ww.titleNum = searchKeyword(title,keyWord)
    #content
    content = getContent(soup)
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
    ww.printWordResult()
    #b = time.time()
    #print('search keyword time:', b-a)
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

def downloadPage(filename, forumName, page, link):
    a = time.time()
    pageText = getPageText(link)
    b = time.time()
    directory = 'ptt/'+forumName+'/'+str(page)+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(directory+str(page)+'_'+filename+".txt","w")
    f.write(link+'\n'+pageText)
    f.close()
    print('download time:', round(b-a, 2))

def searchForum(forumName, startPage, totalPage, keyWord):
    pageNum=startPage
    N=totalPage
    for i in range(N): # 翻頁N次
        prevPage='https://www.ptt.cc/bbs/'+forumName+'/index'+str(pageNum)+'.html'
        print('page', pageNum)
        pageText = getPageText(prevPage)

        soup = BeautifulSoup(pageText, 'lxml')
        articles = soup.find_all('div', 'r-ent')

        NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
                                 
        for article in articles:
            meta = article.find('div', 'title').find('a') or NOT_EXIST
            if(meta != NOT_EXIST):
                articleCount += 1
                link = meta.get('href') 
                print(link)

                searchPage('https://www.ptt.cc'+link, keyWord)
        #next page
        pageNum -= 1

def downloadForum(forumName, startPage, totalPage):
    pageNum=startPage
    N=totalPage
    for i in range(N): # 翻頁N次
        articleCount=0
        prevPage='https://www.ptt.cc/bbs/'+forumName+'/index'+str(pageNum)+'.html'
        print('page', pageNum)
        pageText = getPageText(prevPage)

        soup = BeautifulSoup(pageText, 'lxml')
        articles = soup.find_all('div', 'r-ent')

        NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
                                 
        for article in articles:
            meta = article.find('div', 'title').find('a') or NOT_EXIST
            if(meta == NOT_EXIST):
                link = 'empty' 
                print(link)
                downloadPage(str(articleCount), forumName, pageNum, link) #empty page
            else:
                link = meta.get('href') 
                print(link)
                downloadPage(str(articleCount), forumName, pageNum, 'https://www.ptt.cc'+link)
            articleCount += 1
        #next page
        pageNum -= 1

#main
def main(argv):
    start = time.time()
    if(argv[0] == '-d'):
        if(len(argv)!= 4):
            print('usage: -d "forumName" "startPage" "number of pages"')
            sys.exit()
        else:
            forumName = argv[1]
            startPage = int(argv[2])
            pages = int(argv[3])

        #download forum from web
        downloadForum(forumName, startPage, pages)
    else:
        print('option not correct')
        sys.exit()
    #search forum from web
    #keyword='推'
    #searchForum('Gossiping', startPage, pages, keyword)

    #search from text file
    '''
    totalPage = 18
    for i in range(totalPage):
        file = open(foldername+'/'+str(i)+'.txt', 'r')
        searchText(file.read(), keyword)
    '''
    end = time.time()
    print('time:', end - start, 'seconds')

if __name__ == '__main__':
    main(sys.argv[1:])
    