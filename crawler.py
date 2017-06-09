import requests
#from multiprocessing import Process
from bs4 import BeautifulSoup
import time
import dataIO
import sys, os

def getPageText(link):
    #a = time.time()
    if(link == 'empty'):
        pageText='This page has been deleted.'
    else:
        pageText=requests.get(link, cookies={'over18':'1'}, timeout = 2).text
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
    return searchText(t, keyWord)

# search from file
def searchText(text,keyWord):
    #a = time.time()
    ww = dataIO.WordResultWrapper(keyWord)
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
    filePath = directory+str(page)+'_'+filename+".txt"
    f = open(filePath, 'w')
    f.write(link+'\n'+pageText)
    f.close()
    print(' download to %s, time: %f' % (filePath, round(b-a, 2)))

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
                #articleCount += 1
                link = meta.get('href')
                print(link)

                searchPage('https://www.ptt.cc'+link, keyWord)
        #next page
        pageNum -= 1

def downloadForum(forumName, startPage, totalPage):
    pageNum=startPage
    N=totalPage
    for i in range(N): # 翻頁N次
        if(N % 5 == 0):
            time.sleep(2)
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
                print(link, end='')
                try:
                    downloadPage(str(articleCount), forumName, pageNum, link) #empty page
                except Exception as e:
                    print('Error')
            else:
                link = meta.get('href')
                print(link, end='')
                try:    
                    downloadPage(str(articleCount), forumName, pageNum, 'https://www.ptt.cc'+link)
                except Exception as e:
                    print('Error')
            articleCount += 1
        #next page
        pageNum -= 1

#main
def main():
    if(len(sys.argv) == 1): # no option
        argv = ['-h']
    else:
        argv=sys.argv[1:]
    
    u_help = '-h'
    u_download = '-d "forumName" "startPage" "number of pages"'
    u_search = ['-s -w "forumName" "startPage" "number of pages"', 
                '-s -f "forumName" "startPage" "number of pages"']

    if(argv[0] == '-h'):
        print('[OPTION]    | [USAGE]') 
        print('HELP        |', u_help)
        print('DOWNLOAD    |', u_download)
        print('SEARCH      |')
        print(' -from web  |', u_search[0])
        print(' -from file |', u_search[1])
    elif(argv[0] == '-d'):
        if(len(argv) != 4):
            print('usage:', u_download)
            sys.exit()
        else:
            start = time.time()
            forumName = argv[1]
            startPage = int(argv[2])
            pages = int(argv[3])
            #download forum from web
            downloadForum(forumName, startPage, pages)
            end = time.time()
            print('time:', end - start, 'seconds')

    elif(argv[0] == '-s'):
        # -s -w/-f "forumName" "startPage" "number of pages"
        usage = 'usage: -s -w/-f "forumName" "startPage" "number of pages"'
        keyword='推'
        if(len(argv) != 5):
            print(usage)
            sys.exit()

        forumName = argv[2]
        startPage = int(argv[3])
        pages = int(argv[4])
        if(argv[1] == '-w'):
            #search from web
            searchForum(forumName, startPage, pages, keyword)
        elif(argv[1] == '-f'):
            #search from text file
            directory = 'ptt/' + forumName + '/'
            for j in range(startPage, startPage+pages):
                for i in range(20):
                    file = open(directory+str(j)+'_'+str(i)+'.txt', 'r')
                    searchText(file.read(), keyword)
                    file.close()
        else:
            print(usage)
            sys.exit() 

    else:
        print('option not correct')
        sys.exit()

    

if __name__ == '__main__':
    main()

