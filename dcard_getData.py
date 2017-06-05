# -*- coding: utf-8 -*-
"""
Psychoinfomatics and Neuroinformatics
Final Project
NTUEE3 B03901014 Ya-Liang Chang
NTUEE3 B03
"""

from dcard import Dcard
import pickle
import re
from dataIO import TypeResultWrapper, WordResultWrapper

def help_message():
    print ("Psychoinfomatics and Neuroinformatics")
    print ("Final Project")
    print ("NTUEE3 B03901014 Ya-Liang Chang")
    print ("NTUEE3 B03901")
    print (" ")

def hot(metas):
    #return [m for m in metas if m['likeCount'] >= 10]
    return [m for m in metas if "圖" in m['title'] and m['likeCount'] > 100]
def getWordToFind():
    wordToFindList = []
    wordToFindList.append("婊")
    return wordToFindList

"""
Find discriminative words in all articles on Dcard.
"""
def get_words(metas):
    filteredMetas = []
    wordToFindList = getWordToFind()

    print ("")
    count = 1;
    for m in metas:
        for eachWord in wordToFindList:
            if eachWord in m['title']:
                print (m['title'], end="\r")
                print ("")
                filteredMetas.append(m)
        print ("Searching %d ..." % count, end="\r")
        count += 1
    print ("")

    return filteredMetas
"""
class TypeResultWrapper:

    def __init__(self, type_):
        self.typeName = type_
        self.wordList = []

    def addWord(self, wordResultWrapper):
        self.wordList.append(wordResultWrapper)

    def printTypeResult(self):
        print ("")
        print ("#%s" % self.typeName)
        for eachWord in self.wordList:
            eachWord.printWordResult()

class WordResultWrapper:

    def __init__(self, word):
        self.wordName = word
        self.titleNum = 0
        self.contentNum = 0
        self.commentNum = 0


    def printWordResult(self):
        #Remove white space for Chinese characters
        wordLen = len(self.wordName)
        #English
        if len(self.wordName) == len(self.wordName.encode()):
            wordLen = 0
        print ("%-*s %8d %8d %8d" % ((8-wordLen), self.wordName, self.titleNum, self.contentNum, self.commentNum))

"""
class DcardWrapper:

    def __init__(self):
        self.dcard = Dcard()
        self.word_list_dict = dict() #a dict with {"品德": ["母豬", "妓女"...], ...}
        self.forum_list = None
        self.searching_num = 5
        self.result_list = [] #a list of result dict

    def printResult(self):
        print ("")
        print ("%-8s %8s %8s %8s" % ("Word in", "Title", "Content", "Comment"))
        for eachType in self.result_list:
            eachType.printTypeResult()

    def readTextList(self, text_list_file):
        text_list = text_list_file.read().split('\n')

        print ("Text from file: ")
        print (text_list)
        listLen = len(text_list)
        i = 0
        while i  < listLen:
            if "#" in text_list[i]:
                type_name = text_list[i].split("#")[1]
                i += 1
                a_word_type = []
                while (text_list[i] != ''):
                    a_word_type.append(text_list[i])
                    i += 1
                self.word_list_dict[type_name] = a_word_type
            elif text_list[i] == '':
                i += 1
            else:
                raise IOError("Error in read file, line %d: %s" % (i, text_list[i]))

        print ("Word list dictionary read: ")
        print (self.word_list_dict)

    def readForumList(self, forum_list_file):
        self.forum_list = forum_list_file.read().split('\n')


    def readWordListDict(self):
        with open("word_list_female.dat", 'rb') as read_file:
            self.word_list_dict = pickle.load(read_file)

    def writeWordListDict(self):
        with open("word_list_female.dat", 'wb') as write_file:
            pickle.dump(self.word_list_dict, write_file)



    def getWordDataFromForum(self, forumName):
        #metadata_forums = dcard.forums.get()
        """
        for each in metadata_forums:
            print (each['name'])
            print (each['alias'])
        forumName = 'relationship'
        forumName = 'girl'
        word = '婊'
        """
        f = self.dcard.forums(forumName)
        print (self.searching_num, "Meta collecting ...", end=' ')
        m = f.get_metas(num=self.searching_num)#, callback=get_words) #list
        print ("Done.")
        print ("Posts collecting ...", end=' ')
        p = self.dcard.posts(m).get(links=False)
        print ("Done.")
        print ("Result parsing ...", end=' ')
        result = p.result()
        print ("Done.")
        for typeName, wordList in self.word_list_dict.items():
            typeResultWrapper = TypeResultWrapper(typeName)
            print ("")
            print ("#Type: ", typeName)
            for eachWord in wordList:
                wordResultWrapper = WordResultWrapper(eachWord)

                count = 0
                for eachPost in result:
                    print ("Searching %s in %s ...  %d / %d " % (eachWord, forumName, count, len(result)), end='\r')
                    count += 1
                    #print (eachPost['comments'])
                    wordInTitles = re.findall(eachWord, eachPost['title'])
                    if wordInTitles:
                        wordResultWrapper.titleNum += len(wordInTitles)
                    wordInContent = re.findall(eachWord, eachPost['content'])
                    if wordInContent:
                        wordResultWrapper.contentNum += len(wordInContent)
                    for eachComment in eachPost['comments']:
                        if eachComment['hidden']:
                            wordInComment = re.findall(eachWord, eachComment['content'])
                            if not wordInComment:
                                wordResultWrapper.commentNum += len(wordInComment)

                print ("Searching %s in %s ...  %d / %d " % (eachWord, forumName, count, len(result)))
                typeResultWrapper.addWord(wordResultWrapper)
            self.result_list.append(typeResultWrapper)
        self.printResult()

def main():
    dcardWrapper = DcardWrapper()
    with open('word_list_female.txt', 'r') as text_list_file:
        dcardWrapper.readTextList(text_list_file)
    dcardWrapper.getWordDataFromForum('sex')

    #data_to_write_file =

if __name__ == "__main__":
    main()
"""
    #print (eachPost)
    wordToFind = "婊"
    if wordToFind in eachPost['title']:
        print (eachPost['title'])
    for eachComment in eachPost:
        if wordToFind in eachComment:
            print (eachComment)
    #print ('\t', eachPost['id'], eachPost['title'])#, eachPost['tags'])
    """


"""
import urllib.request,json
u='https://www.dcard.tw/_api/posts/226048661'
r=urllib.request.Request(u,headers={'User-Agent':''})
data=urllib.request.urlopen(r).read()
j_data=json.loads(data.decode('utf-8'))
print(j_data['media'][0]['url'])
for key in j_data.keys():
    print(key,':',j_data[key])
"""
"""
import pickle
print romanD
file = open("roman1.dat", "w")
pickle.dump(romanD1, file)
file.close()
file = open("roman1.dat", "r")
romanD2 = pickle.load(file)
file.close()
print "Dictionary after pickle.dump() and pickle.load():"
print romanD2
"""
