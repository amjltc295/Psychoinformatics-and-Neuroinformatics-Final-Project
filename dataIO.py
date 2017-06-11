import pickle
import sys


def readTextList(text_list_file):
    text_list = text_list_file.read().split('\n')

    print ("Text from file: ")
    listLen = len(text_list)
    word_list_dict = dict()
    i = 0
    while i  < listLen:
        if "#" in text_list[i]:
            type_name = text_list[i].split("#")[1]
            i += 1
            a_word_type = []
            while (text_list[i] != ''):
                if not ( '/' in text_list[i] ):
                    a_word_type.append(text_list[i])
                i += 1
            word_list_dict[type_name] = a_word_type
        elif text_list[i] == '':
            i += 1
        else:
            raise IOError("Error in read file, line %d: %s" % (i, text_list[i]))

    print ("Word list dictionary read: ")
    print (word_list_dict)
    return word_list_dict

def readForumList(forum_list_file):
    forum_list = forum_list_file.read().split('\n')
    return forum_list


def readPickle(filename):
    with open(filename, 'rb') as read_file:
        fileContent = pickle.load(read_file)
    print ("Read pickle from %s" % filename)
    return fileContent

def writePickle(filename, content):
    with open(filename, 'wb') as write_file:
        pickle.dump(content, write_file)
    print ("Write pickle into '%s'" % filename)

def readWordListDict(word_list_pickle_file):
    with open(word_list_pickle_file, 'rb') as read_file:
        word_list_dict = pickle.load(read_file)
    return word_list_dict

def writeWordListDict(word_list_pickle_file, word_list_dict):
    with open(word_list_pickle_file, 'wb') as write_file:
        pickle.dump(word_list_dict, write_file)


class TypeResultWrapper:

    def __init__(self, type_):
        self.typeName = type_
        self.wordList = []

    def addWord(self, wordResultWrapper):
        self.wordList.append(wordResultWrapper)

    def printTypeResult(self, toFile=sys.stdout):
        print ("", file=toFile)
        print ("#%s" % self.typeName, file=toFile)
        for eachWord in self.wordList:
            eachWord.printWordResult(toFile)

class WordResultWrapper:

    def __init__(self, word):
        self.wordName = word
        self.titleNum = 0
        self.contentNum = 0
        self.commentNum = 0
        self.postNum = 0 # Count just once in each post
        self.fromMale = 0
        self.fromFemale = 0
        self.numInEachMonth = dict()
        """ For PTT usage. """
        self.articleCount = 0
        self.commentCount = 0
    def printWordResult(self, toFile=sys.stdout):
        #Remove white space for Chinese characters
        wordLen = len(self.wordName)
        #English
        if len(self.wordName) == len(self.wordName.encode()):
            wordLen = 0
        print ("%-*s %8d %8d %8d %8d %8d %8d %d"
                % ((8-wordLen), self.wordName, self.titleNum, self.contentNum, self.commentNum, (self.titleNum+self.contentNum+self.commentNum), self.fromMale, self.fromFemale, self.postNum),
                file=toFile)
        #self.printWordResultWithTime(toFile)

    def printWordResultWithTime(self, toFile=sys.stdout):
        if (self.numInEachMonth):
            print ("Time    Num", file=toFile)
            for year_month, num in self.numInEachMonth.items():
                print ("%6s %d" % (year_month, num), file=toFile)
        """
        else:
            print ("No result with time")
        """

    def addResult(self, place, num, gender="", time=""):
        if (place == "title"):
            self.titleNum += 1
        elif (place == "content"):
            self.contentNum += num
        elif (place == "comment"):
            self.commentNum += num
        if (gender == 'M'):
            self.fromMale += num
        elif (gender == 'F'):
            self.fromFemale += num
        year = int(time[:4])
        month = int(time[5:7])
        year_month = year*100 + month
        if (year_month in self.numInEachMonth):
            self.numInEachMonth[year_month] += 1
        else:
            self.numInEachMonth[year_month] = 1





