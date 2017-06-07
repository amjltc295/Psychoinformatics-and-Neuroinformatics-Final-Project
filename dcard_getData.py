# -*- coding: utf-8 -*-
"""
Psychoinfomatics and Neuroinformatics
Final Project

Find discriminative words in all articles on Dcard.

NTUEE3 B03901014 Ya-Liang Chang
NTUEE3 B03901015 Hsi-Sheng Mei
"""

from dcard import Dcard
#import pickle
import re
#from dataIO import TypeResultWrapper, WordResultWrapper
import dataIO
import os, sys

def help_message():
    print ("Usage: python dcard_getData.py <forum name> <number of articles to search>")
    print ("")

def welcome_message():
    print ("Psychoinfomatics and Neuroinformatics")
    print ("Final Project")
    print ("NTUEE3 B03901014 Ya-Liang Chang")
    print ("NTUEE3 B03901015 Hsi-Sheng Mei")
    print (" ")



class DcardWrapper:

    def __init__(self):
        self.dcard = Dcard()
        self.word_list_dict = dict() #a dict with {"品德": ["母豬", "妓女"...], ...}
        self.forum_list = None
        self.searching_num = 10
        self.raw_result = list()
        self.result_list = [] #a list of result dict
        self.currentForum = ""

    def printInfo(self):
        print ("")
        print ("Forum: %s" % self.currentForum)
        print ("Number of articles to search: %d" % self.searching_num)

    def printResult(self):
        print ("")
        print ("%-8s %8s %8s %8s %8s %8s" % ("Word in", "Title", "Content", "Comment", "Male", "Female"))
        for eachType in self.result_list:
            eachType.printTypeResult()



    def getWordDataFromForum(self, forumName, searching_num):
        self.searching_num = searching_num
        self.currentForum = forumName
        self.printInfo()
        #metadata_forums = dcard.forums.get()
        """
        for each in metadata_forums:
            print (each['name'])
            print (each['alias'])
        forumName = 'relationship'
        forumName = 'girl'
        word = '婊'
        """
        print ("")
        if not ( self.read_raw_result(forumName)):
            f = self.dcard.forums(forumName)
            print (self.searching_num, "Meta collecting ...", end=' ', flush=True)
            m = f.get_metas(num=self.searching_num)#, callback=get_words) #list
            print ("Done.")
            print ("")
            print ("Posts collecting ...", end=' ', flush=True)
            p = self.dcard.posts(m).get(links=False)
            print ("Done.")
            print ("")
            #result = [ next(p.results) for i in range(self.searching_num)]
            #result = []
            #print (type(next(p.results)))
            #print (next(p.results))
            #print (next(p.results))
            """
            for each in p.results:
                print (each)
                input("a:")
            """
            #print ("Result parsing ...", end=' ', flush=True)
            #result = p.result()
            #result = p.results
            #print ("Done.")
        for typeName, wordList in self.word_list_dict.items():
            typeResultWrapper = dataIO.TypeResultWrapper(typeName)
            print ("")
            print ("#Type: ", typeName)
            for eachWord in wordList:
                wordResultWrapper = dataIO.WordResultWrapper(eachWord)

                count = 0
                while count < self.searching_num or self.searching_num == -1:

                    if len(self.raw_result) == self.searching_num:
                        eachPost = self.raw_result[count]
                        print ("Searching %s in %s ...  %d / %d " % (eachWord, forumName, count, self.searching_num), end='\r', flush=True)
                    else:
                        try:
                            eachPost = next(p.results)
                            self.raw_result.append(eachPost)
                        except:
                            self.searching_num = len(self.raw_result)
                            break
                        else:
                            print ("Downloading data and searching %s in %s ...  %d / %d " % (eachWord, forumName, count, self.searching_num), end='\r', flush=True)

                #for eachPost in result:
                    count += 1
                    #print (eachPost['comments'])
                    try:
                        wordInTitles = re.findall(eachWord, eachPost['title'])
                    except:
                        print ("")
                        print ("Error key title", eachPost)
                        continue
                    else:
                    #if wordInTitles:
                        try:
                            wordResultWrapper.titleNum += len(wordInTitles)

                            if eachPost['gender'] == 'M':
                                wordResultWrapper.fromMale += len(wordInTitles)
                            elif eachPost['gender'] == 'F':
                                wordResultWrapper.fromFemale += len(wordInTitles)
                        except:
                            print ("")
                            print ("Error in title",  eachPost['title'])
                            continue

                    try:
                        wordInContent = re.findall(eachWord, eachPost['content'])
                    except:
                        print ("")
                        print ("Error key content", eachPost)
                        continue

                    if wordInContent:
                        try:
                            wordResultWrapper.contentNum += len(wordInContent)
                            if eachPost['gender'] == 'M':
                                wordResultWrapper.fromMale += len(wordInContent)
                            elif eachPost['gender'] == 'F':
                                wordResultWrapper.fromFemale += len(wordInContent)
                        except:
                            print ("")
                            print ("Error in wordInContent: ", wordInContent)
                            print ("Post: ", eachPost['content'])
                            continue

                    for eachComment in eachPost['comments']:
                        try:
                            if not eachComment['hidden']:
                                wordInComment = re.findall(eachWord, eachComment['content'])
                                if not wordInComment:
                                    wordResultWrapper.commentNum += len(wordInComment)
                                    if eachComment['gender'] == 'M':
                                        wordResultWrapper.fromMale += len(wordInComment)
                                    elif eachComment['gender'] == 'F':
                                        wordResultWrapper.fromFemale += len(wordInComment)
                        except:
                            print ("")
                            print ("Error in eachComment", eachComment)
                            print ("")

                print ("Searching %s in %s ...  %d / %d               " % (eachWord, forumName, self.searching_num, self.searching_num))
                typeResultWrapper.addWord(wordResultWrapper)
            self.result_list.append(typeResultWrapper)
        self.printResult()
        self.write_raw_result(forumName)

    def write_raw_result(self, forumName):
        if not os.path.exists('./data'):
            os.makedirs('data')
        filename = 'data/%s_%d_raw_result.dat' % (forumName, self.searching_num)
        if not os.path.isfile(filename):
            dataIO.writePickle(filename, self.raw_result)

    def read_raw_result(self, forumName):
        filename = 'data/%s_%d_raw_result.dat' % (forumName, self.searching_num)
        if os.path.isfile(filename):
            self.raw_result = dataIO.readPickle(filename)
            return True
        else:
            return False


def main(argv):
    if len(argv) < 2:
        help_message()
    else:
        welcome_message()
        dcardWrapper = DcardWrapper()
        forumName = argv[0]
        searching_num =  int(argv[1]) if argv[1] != 'i' else dcardWrapper.dcard.forums.infinite_page
        with open('word_list_female.txt', 'r') as text_list_file:
            dcardWrapper.word_list_dict = dataIO.readTextList(text_list_file)
        dcardWrapper.getWordDataFromForum(forumName, searching_num)


if __name__ == "__main__":
    main(sys.argv[1:])
