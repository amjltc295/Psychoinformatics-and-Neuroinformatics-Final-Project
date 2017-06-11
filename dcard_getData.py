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
        self.totalPostNum = 0
        self.totalCommentNum = 0
        self.commentFromMale= 0
        self.commentFromFemale = 0
        self.raw_result = list()
        self.result_list = [] #a list of result dict
        self.currentForum = ""
        self.currentTitleTopic = ""

    def printInfo(self):
        print ("")
        print ("Forum: %s" % self.currentForum)
        print ("Number of articles to search: %d" % self.searching_num)

    def printResult(self, toFile=sys.stdout):
        print ("Forum: %s" % self.currentForum, file=toFile)
        if (self.currentTitleTopic):
            print ("Finding %s in title only." % self.currentTitleTopic, file=toFile)
        print ("Total %d posts" % self.totalPostNum, file=toFile)
        print ("Total %d comments (male %d / female %d)" % (self.totalCommentNum, self.commentFromMale, self.commentFromFemale), file=toFile)
        print ("%-8s %8s %8s %8s %8s %8s %8s" % ("Word in", "Title", "Content", "Comment", "Total", "Male", "Female"), file=toFile)
        for eachType in self.result_list:
            eachType.printTypeResult(toFile)



    def getDataFromForum(self, forumName, searching_num):
        """ Download posts data from forum. """
        self.searching_num = searching_num
        self.currentForum = forumName

        if not (self.read_raw_result(forumName)):
            f = self.dcard.forums(forumName)
            print (self.searching_num, "Meta collecting ...", end=' ', flush=True)
            m = f.get_metas(num=self.searching_num)#, callback=get_words) #list
            print ("Done.")
            print ("")
            print ("Posts collecting ...", end=' ', flush=True)
            p = self.dcard.posts(m).get(links=False)
            print ("Done.")
            print ("")


            count = 0
            """ Searching the word in each articles, including title, cotent and comments. """
            while count < self.searching_num or self.searching_num == -1:
                try:
                    eachPost = next(p.results)
                    self.raw_result.append(eachPost)
                except:
                    self.searching_num = len(self.raw_result)
                    break
                else:
                    print ("Downloading data in %s ...  %d / %d " % (forumName, count, self.searching_num), end='\r', flush=True)

                if (count % 20000 == 0 and count > 1):
                    self.write_raw_result(forumName)
                    self.raw_result = []
                count += 1

            print ("Downloading data in %s ...  %d / %d     Done."
                    % (forumName, self.searching_num, self.searching_num), end='\r', flush=True)

        else:
            print ("Error in getDataFromForum(): already download.")
            return False
        self.write_raw_result(forumName)

    def searchWordFromData(self, forumName, searching_num, titleTopic=""):
        self.searching_num = searching_num
        self.currentForum = forumName
        self.currentTitleTopic = titleTopic
        self.printInfo()
        print ("")
        """ Download if no data found. """
        if not ( self.read_raw_result(forumName)):
            self.getDataFromForum(forumName, searching_num)

        first_word = True #To count post num and comment num
        for typeName, wordList in self.word_list_dict.items():
            typeResultWrapper = dataIO.TypeResultWrapper(typeName)
            print ("")
            print ("#Type: ", typeName)
            for eachWord in wordList:
                wordResultWrapper = dataIO.WordResultWrapper(eachWord)
                count = 0
                """ Searching the word in each articles, including title, cotent and comments. """
                while count < self.searching_num:
                    wordInTitles = wordInContent = wordInComment = []
                    wordInPost = 0
                    if not len(self.raw_result) == self.searching_num:
                        print ("ERROR in seaching: searching num %d > data num %d"
                                % (self.searching_num, len(self.raw_result)))
                        print ("Turn searching num into data num")
                        print ("")
                        self.searching_num = len(self.raw_result)
                    eachPost = self.raw_result[count]
                    print ("Searching %s in %s ...  %d / %d "
                            % (eachWord, forumName, count, self.searching_num), end='\r', flush=True)

                    """ There are errors to handle when getting large amount of data. """
                    count += 1
                    # Filter those with specific topic in title
                    if (titleTopic != ""):
                        try:
                            if not (titleTopic in eachPost['title']):
                                continue
                        except:
                            print ("")
                            print ("Error in title, post: ",  eachPost)
                            continue

                    # Searching word in titile
                    try:
                        wordInTitles = re.findall(eachWord, eachPost['title'])
                        self.totalPostNum += 1 if first_word else 0
                    except:
                        print ("")
                        print ("Error key title, post: ", eachPost)
                        continue
                    if wordInTitles:
                        wordInPost = 1
                        try:
                            wordResultWrapper.addResult('title', len(wordInTitles),
                                    eachPost['gender'], eachPost['createdAt'])
                        except:
                            print ("")
                            print ("Error in title: ",  eachPost['title'])
                            continue

                    # Searching word in content of posts
                    try:
                        wordInContent = re.findall(eachWord, eachPost['content'])
                    except:
                        print ("")
                        print ("Error key content, post: ", eachPost)
                        continue

                    if wordInContent:
                        wordInPost = 1
                        try:
                            wordResultWrapper.addResult('content', len(wordInContent),
                                    eachPost['gender'], eachPost['createdAt'])
                        except:
                            print ("")
                            print ("Error in wordInContent, post: ", eachPost['content'])
                            continue

                    # Searching word in comments of posts
                    for eachComment in eachPost['comments']:
                        try:
                            if not eachComment['hidden']:
                                if first_word:
                                    self.totalCommentNum += 1
                                    if eachComment['gender'] == 'M':
                                        self.commentFromMale += 1
                                    elif eachComment['gender'] == 'F':
                                        self.commentFromFemale += 1
                                    else:
                                        #Some comment without gender or from official
                                        self.totalCommentNum -= 1

                                wordInComment = re.findall(eachWord, eachComment['content'])
                                if wordInComment:
                                    wordInPost = 1
                                    wordResultWrapper.addResult('comment', len(wordInComment),
                                            eachComment['gender'], eachComment['createdAt'])
                        except:
                            print ("")
                            print ("Error in searching eachComment: ", eachComment)
                    if (wordInPost):
                        wordResultWrapper.postNum += 1


                print ("Searching %s in %s ...  %d / %d                  Done."
                        % (eachWord, forumName, self.searching_num, self.searching_num))
                typeResultWrapper.addWord(wordResultWrapper)
                first_word = False
            self.result_list.append(typeResultWrapper)
        print ("End of searching")
        print ("")
        self.printResult()

        directory = 'Dcard/result/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = directory + '%s_%d_result%s.txt' % (self.currentForum, self.searching_num, titleTopic)
        if os.path.isfile(filename):
            print ("Warning: file %s already exists" % filename)
            input("Continue?")
        print ("File %s written." % filename)

        with open(filename, 'w') as outFile:
            self.printResult(outFile)
        #self.writeResult()


    def write_raw_result(self, forumName):
        if not os.path.exists('./data'):
            os.makedirs('data')
        filename = 'data/%s_%d_raw_result.dat' % (forumName, self.searching_num)
        if not os.path.isfile(filename):
            dataIO.writePickle(filename, self.raw_result)
        else:
            print ("File %s already exists" % filename)

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
        with open('word_list.txt', 'r') as text_list_file:
            dcardWrapper.word_list_dict = dataIO.readTextList(text_list_file)
        if (len(argv) == 2):
            dcardWrapper.searchWordFromData(forumName, searching_num)
        else:
            dcardWrapper.searchWordFromData(forumName, searching_num, argv[2])


if __name__ == "__main__":
    main(sys.argv[1:])
