class TrieNode:
    def __init__(self):
        self.children = {}      #Using Hashmap instead of an array because it's more efficient
        self.endOfWord = False  #Indicate if it's the end of a word
        self.locs = []

class Trie:
    def __init__(self, documents=[]):
        self.root = TrieNode() #Initializing root node for the Trie
        
        # Adds all the documents to the trie
        for doc in documents:
            for word in doc.wordsTuples:
                self.insert(word[0], word[1])

    def insert(self, word:str, locs) -> None:
        curr = self.root                            #Start with the root node

        for char in word:                           #For every character in the word
            if char not in curr.children:           #If the character does not exist
                curr.children[char] = TrieNode()    #then make a new node of that character
            curr = curr.children[char]              #Make curr the next character node that already exists or was created
        curr.endOfWord = True                       #Mark that the word ends here

        #Add location
        curr.locs.append(locs)

    def search(self, word:str) -> bool:
        curr = self.root                    #Start with the root node

        for char in word:                   #For every character in the word
            if char not in curr.children:   #If the character does not exist
                return False                #The word does not exist
            curr = curr.children[char]      #Make curr the next character node if that character exists
        return curr.endOfWord               #The word exists

    def prefixExists(self, prefix: str) -> bool:
        curr = self.root                        #Start with the root node

        for char in prefix:                     #For every character in the word
            if char not in curr.children:       #If the character does not exist
                return False                    #The prefix does not exist
            curr = curr.children[char]          #Make curr the next character node if that character exists
        return True                             #The prefix exists

    def _prefixSearchHelper(self, word, curr):
        if curr.endOfWord:      #If there is a delimeter node then append the word to the hashmap
            self._prefixWords[word] = curr.locs

        for char, node in curr.children.items():
            self._prefixSearchHelper(word + char, node) 

    #prefixSearch
    def prefix_complete(self, prefix: str) -> list:
        curr = self.root                        #Start with the root node

        for char in prefix:                     #For every character in the word
            if char not in curr.children:       #If the character does not exist
                return {}                       #The prefix does not exist
            curr = curr.children[char]          #Make curr the next character node if that character exists

        self._prefixWords = {}                  #An empty hashmap for the list of words returneed by the prefix search
        self._prefixSearchHelper(prefix, curr)

        return self._prefixWords