import math

class InvertedIndex:
    def __init__(self, documents=[]) -> None:
        self.index = {} 
        self.documents = documents
        self.totalDocuments = len(documents) #Total number of documents

        uniqueword = {} #Key: Word, Value: Word Frequency in all documents
        InverseDocumentFrequency = {} #Key: Word, Value: IDF of word
        totalwordsindocument = {} #Key: DocumentName, Value: total words in document

        for doc in documents:

            totalwordsindocument[doc.docId] = len(doc.wordsTuples)
        
            for key in doc.wordsTuples: # wordsTuples consists of a list
                                        # of tuples of all the words and their corresponsing
                                        # index in the document

                if uniqueword.get(key[0]) == None: # If key[0] is not in uniqueword             
                    uniqueword[key[0]] = 1         # Add it in dictionary with value 1
                else:
                    uniqueword[key[0]] += 1        # If present increase value by 1

        un = {} #Key: Word, Value: How many documents it appears in

        for i in uniqueword:
            count = 0

            for doc in documents:

                if i in doc.wordsDict.keys(): #If i is in the Document increase count by 1

                    count = count + 1         

            un[i] = count

        
        ind = {} # Key: Word,  Value: Index
        ind2 = {}  # Key: Index, Value: Word
        i = 0
        #Calculates the IDF of each word
        for word in uniqueword: 

            if un[word] < len(documents): #If Word appears in every document IDF = 0
                InverseDocumentFrequency[word] = math.log10(self.totalDocuments / un[word] )
            else:
                InverseDocumentFrequency[word] = 0
        
        
            ind[word] = i 
            ind2[i] = word
            i += 1

        wordfrequency = [] 
        
        temp = []
        for doc in documents:

            wordfreqperdoc = [0] * len(uniqueword)

            for i in doc.wordsTuples:
                index = ind[i[0]]
                wordfreqperdoc[index] += 1

            wordfrequency.append(wordfreqperdoc) #A list of lists which contain the frequency
            # of every word in every document

            temp.append([0] * len(uniqueword))

        for i in range(self.totalDocuments):
            for j in range(len(uniqueword)):
                wf = wordfrequency[i][j] 
                temp[i][j] = (wf / totalwordsindocument[documents[i].docId]) * InverseDocumentFrequency[ind2[j]] 
                # calculates the tf-idf of each word in every document

        # Key: Word,  Value: Index
        self.indexes = ind
        # Key: Index, Value: Word
        self.indexes2 = ind2

        self.tfidf = temp
        

    def query(self, query, num):

        temp = {}

        querylist = query.split()
        
        for w in querylist:
            docnum = 0
            for i in self.tfidf:
                if self.documents[docnum].wordsDict.get(w) != None:
                    index = self.indexes[w]
                    if temp.get(self.documents[docnum].docId) == None:
                        temp[self.documents[docnum].docId] = i[index]
                    else:
                        temp[self.documents[docnum].docId] += i[index]

                docnum += 1

        temp = list(temp.items())

        temp.sort(key = lambda x: x[0], reverse = True)

        final = []
        
        if num > len(temp):
            num = len(temp)

        for l in range(0, num):
            final.append((l+1, temp[l][0][7:]))

        return final