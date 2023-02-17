import os
import re
import pathlib
import math
from zipfile import ZipFile, is_zipfile
from pprint import pprint
from trie import *
from index import *


class Document:
    def __init__(self, docId, data):
        self.docId = docId
        self.data = data
        self._tokenize()

    def _tokenize(self):
        self.words = []
        self.wordsDict = {}
        self.wordsTuples = []
        #Reference: https://www.geeksforgeeks.org/python-program-to-find-start-and-end-indices-of-all-words-in-a-string/
        for word in re.finditer(r'\S+', self.data):
            #append word to the list of words in the document
            self.words.append(word.group(0))

            # To generate dictionary in the format {Word: [(Document ID, Starting Index, Ending Index)]..}
            if self.wordsDict.get(word.group(0)) == None:
                self.wordsDict[word.group(0)] = [(word.start(), word.end())]
            else:
                self.wordsDict[word.group(0)].append((word.start(), word.end()))
            
            # To generate list of words in the format (Word, (Document ID, Starting Index, Ending Index))
            wordTuple = [word.group(0).lower(), ((self.docId, word.start(), word.end()))]

            self.wordsTuples.append(wordTuple)

class Corpus:
    def __init__(self, path) -> None:

        listofdocs = []
        
        self.documents = []
        
        if is_zipfile(path):
            #Reference: https://www.geeksforgeeks.org/working-zip-files-python/
            file = ZipFile(path, mode = 'r')
            filePaths = file.namelist()
            file.extractall() 
        elif os.path.isdir(path):
            #files = os.listdir(path)
            #Reference: https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
            filePaths = list()
            for (dirpath, dirnames, filenames) in os.walk(path):
                filePaths += [os.path.join(dirpath, file) for file in filenames]
        else:
            filePaths = [path]
        
        for filePath in filePaths:
            if os.path.isfile(filePath):
                with open(filePath, 'r',encoding='ascii' , errors = 'ignore') as f:

                    text = f.read().lower()

                    #Reference: https://datagy.io/python-remove-punctuation-from-string/
                    newtext = re.sub(r'[^\w\s]', '', text)

                # To normalize path for the test cases >:(
                p = filePath
                filePath = pathlib.PureWindowsPath(filePath).as_posix()[len(path):]
                

                doc = Document(filePath, newtext)
                doc2 = Document(p,newtext)

                listofdocs.append(doc2)
                self.documents.append(doc)

        self.trie = Trie(self.documents)  #Creates a Trie object from the corpus
        
        self.index = InvertedIndex(listofdocs)

    def prefix_complete(self, query:str):
        '''
            Turn the query into lowercase since every word in the Corpus is lowercase
            Then call prefix_complete method of the trie object of class Trie to get a list of prefix matches
            Return the list of Prefix Matches
        '''
        return self.trie.prefix_complete(query.lower())

    def query(self, query: str, num):
        return self.index.query(query.lower(), num)
