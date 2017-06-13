import requests
#from multiprocessing import Process
from bs4 import BeautifulSoup
import time
import dataIO
import sys, os

class DateWrapper:
    def __init__(self):
        self.Jun=[]
        self.May=[]
        self.Apr=[]
    def addDate(self, str):
        month=str[:3]
        date=int(str[3:])
        if(month=='Jun'):
            self.Jun.append(date)
        elif(month=='May'):
            self.May.append(date)
        elif(month=='Apr'):
            self.Apr.append(date)
    def printSummary(self):
        for j in range(1,31):
            count=0
            for i in self.Apr:
                if(i==j): count += 1
            print('Apr', j, ':', count)
        print('')
        for j in range(1,32):
            count=0
            for i in self.May:
                if(i==j): count += 1
            print('May', j, ':', count)
        print('')
        for j in range(1,31):
            count=0
            for i in self.Jun:
                if(i==j): count += 1
            print('Jun', j, ':', count)


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
    s=soup.find_all('span', 'article-meta-value')
    return s[2].getText()

def getTitleFromText(text):
    soup = BeautifulSoup(text, 'lxml')
    #title
    return getTitle(soup)

def getContent(soup):
    s=soup.find_all('span', 'f6')
    for i in s:
        i.decompose()

    content = soup.find(id="main-content")
    s1 = content.find_all('div', 'article-metaline')
    for i in s1:
        i.decompose()
    s2 = content.find_all('div', 'article-metaline-right')
    for i in s2:
        i.decompose()

    target_back = '※ 發信站: 批踢踢實業坊(ptt.cc)'
    content = content.text.split(target_back)
    main_content = content[0]
    return main_content

def getDate(text):
    soup = BeautifulSoup(text, 'lxml')
    s=soup.find_all('span', 'article-meta-value')
    timeStr=s[3].text
    date=timeStr[4:10]
    return(date)

# search an article page
def searchPage(link,keyWord,ww):
    t = getPageText(link)
    return searchText(t, keyWord, ww)

# search from file
def searchText(text,keyWord, ww = dataIO.WordResultWrapper(''), multi=True):
    #a = time.time()
    if(ww.wordName == ''):
        ww = dataIO.WordResultWrapper(keyWord)
    soup = BeautifulSoup(text, 'lxml')
    #title
    title = getTitle(soup)
    if(multi):
        n_t = searchMultiKeyword(title,keyWord)
    else:
        n_t = searchKeyword(title,keyWord)
    ww.titleNum += n_t
    #content
    content = getContent(soup)
    if(multi):
        n_ct = searchMultiKeyword(content,keyWord)
    else:
        n_ct = searchKeyword(content,keyWord)
    ww.contentNum += n_ct
    #pushes
    pushes = soup.find_all('div', 'push')
    n_cm_total = 0
    for push in pushes:
        #ptt_id = push.find('span', 'f3 hl push-userid').getText()
        comment = push.find('span', 'f3 push-content').getText()
        if(multi):
            n_cm = searchMultiKeyword(comment,keyWord)
        else:
            n_cm = searchKeyword(comment,keyWord)
        if(n_cm != 0):
            #print(comment)
            ww.commentCount += 1
        n_cm_total += n_cm
    ww.commentNum += n_cm_total

    if(n_t + n_ct + n_cm_total != 0):
        ww.articleCount += 1

    return ww

# search from file
def searchText_Date(text,keyWord, dw, multi=False):
    #a = time.time()
    soup = BeautifulSoup(text, 'lxml')
    #title
    dateStr = getDate(text)
    title = getTitle(soup)
    if(multi):
        n_t = searchMultiKeyword(title,keyWord)
    else:
        n_t = searchKeyword(title,keyWord)
    #content
    content = getContent(soup)
    if(multi):
        n_ct = searchMultiKeyword(content,keyWord)
    else:
        n_ct = searchKeyword(content,keyWord)
    #pushes
    pushes = soup.find_all('div', 'push')
    n_cm_total = 0
    for push in pushes:
        #ptt_id = push.find('span', 'f3 hl push-userid').getText()
        comment = push.find('span', 'f3 push-content').getText()
        if(multi):
            n_cm = searchMultiKeyword(comment,keyWord)
        else:
            n_cm = searchKeyword(comment,keyWord)
        n_cm_total += n_cm

    if(n_t + n_ct + n_cm_total != 0):
        print(dateStr)
        dw.addDate(dateStr)

    return dw

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

def searchMultiKeyword(text,wordList):
    count=0
    for word in wordList:
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

def searchForum(forumName, startPage, totalPage, keyWord, ww):
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

                ww=searchPage('https://www.ptt.cc'+link, keyWord, ww)
        #next page
        pageNum -= 1

def downloadForum(forumName, startPage, totalPage):
    pageNum=startPage
    N=totalPage
    errorCount=0
    for i in range(N): # 翻頁N次
        if(N % 5 == 0):
            time.sleep(2)
        articleCount=0
        prevPage='https://www.ptt.cc/bbs/'+forumName+'/index'+str(pageNum)+'.html'
        print('page', pageNum)
        try:
            pageText = getPageText(prevPage)
        except Exception as e:
            print('Error')
            errorCount += 1
            if(errorCount >= 3):
                pageNum -= 1
            continue

        soup = BeautifulSoup(pageText, 'lxml')
        articles = soup.find_all('div', 'r-ent')

        NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

        for article in articles:
            meta = article.find('div', 'title').find('a') or NOT_EXIST
            if(meta == NOT_EXIST):
                link = 'empty'
                print(link, end='')
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

def downloadMissingPage(forumName, startPage, endPage):
    for page in range(startPage, endPage+1):
        directory = 'ptt/' + forumName + '/' + str(page) + '/'
        if not os.path.isdir(directory):
            try:
                print('page', page, 'missing')
                downloadForum(forumName, page, 1)
            except Exception as e:
                 print('Error')
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
        print(' -from web  |', u_search[0], 'SOME PROBLEMS TO BE FIXED')
        print(' -from file |', u_search[1])
    elif(argv[0] == '-d'):
        if(len(argv) == 5):
            if(argv[1] == '-m'):
                start = time.time()
                forumName = argv[2]
                startPage = int(argv[3])
                endPage = int(argv[4])
                #download forum from web
                downloadMissingPage(forumName, startPage, endPage)
                end = time.time()
                print('time:', end - start, 'seconds')
        elif(len(argv) != 4):
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
        keyword=['母豬', '女森','台女', '74團', '騎士團', '處女']
        #keyword=['渣男']
        #keyword=['母豬']
        #keyword=['74團','騎士團']
        #keyword=['母豬', '女森', '台女']
        #keyword=['甲甲','臭甲']
        #keyword=['奕含','房思琪','陳星','陳興']

        multi=True # multi keyword OR not
        en_titleSearch=True # Use title to filter OR not
        searchDate=False # print date distribution OR word summary

        if(en_titleSearch):
            titleword=['女作家','A女','奕含','房思琪','陳星','陳興','C師']
            #titleword=['女']
        a_count = 0
        if(len(argv) != 5):
            print(usage)
            sys.exit()

        a = time.time()
        ww = dataIO.WordResultWrapper(keyword)
        forumName = argv[2]
        startPage = int(argv[3])
        pages = int(argv[4])
        if(argv[1] == '-w'):
            #search from web
            searchForum(forumName, startPage, pages, keyword, ww)
        elif(argv[1] == '-f'):
            #search from text file
            emptyFile = 0
            directory = 'ptt/' + forumName + '/'
            dw = DateWrapper()
            dw_total = DateWrapper()
            for j in range(startPage, startPage+pages):
                print('page', j)
                for i in range(20):
                    try:
                        file = open(directory+str(j)+'/'+str(j)+'_'+str(i)+'.txt', 'r')
                        text = file.read()
                        title = getTitleFromText(text)
                        if(en_titleSearch):
                            in_title=False
                            for t in titleword:
                                if(title.find(t)!= -1):
                                    #print(t, 'in title')
                                    in_title=True
                            if(in_title):
                                print(title)
                                a_count += 1
                                dateStr=getDate(text)
                                dw_total.addDate(dateStr)
                                if(searchDate):
                                    dw = searchText_Date(text, keyword, dw, multi)
                                else:
                                    ww = searchText(text, keyword, ww, multi)
                        else:
                            if(searchDate):
                                dw = searchText_Date(text, keyword, dw, multi)
                            else:
                                ww = searchText(text, keyword, ww, multi)
                        file.close()
                    except Exception as e:
                        emptyFile += 1
            b = time.time()
            print('Total time:', round(b-a, 2))
            if(searchDate):
                print()
                print('titles that contain:', titleword)
                dw_total.printSummary() #print date the the title has titlewords
                print()
                print('in these articles that contain:', keyword)
                dw.printSummary() #print date that the article has keywords
            else:
                print('Total articles:', pages*20 - emptyFile)
        else:
            print(usage)
            sys.exit()


        print('In', forumName, 'from page', startPage, 'to', startPage+pages-1)
        if(en_titleSearch): print('Total titles that contain', titleword, ':', a_count)
        print('Total', keyword, 'in title:', ww.titleNum)
        print('Total', keyword, 'in content:', ww.contentNum)
        print('Total', keyword, 'in comment:', ww.commentNum)
        print('Total articles that contain', keyword, ':', ww.articleCount)
        print('Total pushes that contain', keyword, ':', ww.commentCount)

    else:
        print('option not correct')
        sys.exit()



if __name__ == '__main__':
    main()

