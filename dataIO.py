import pickle


def readTextList(text_list_file):
    text_list = text_list_file.read().split('\n')

    print ("Text from file: ")
    print (text_list)
    listLen = len(text_list)
    word_list_dict = dict()
    i = 0
    while i  < listLen:
        if "#" in text_list[i]:
            type_name = text_list[i].split("#")[1]
            i += 1
            a_word_type = []
            while (text_list[i] != ''):
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
