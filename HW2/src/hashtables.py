from typing import Any
import random

# set = intial config: (x, y) coordinates of alive cells.
# dict = stores count of live neighbors for cells.

class MySet(object):
    '''An abstract class that provides a set interface which is just sufficient
    for the implementation of this assignment.
    '''

    def __init__(self, elements: [Any]) -> None:
        """Initializes this set with elements.

        Each element in elements must be hashable by python.

        Args:
        - self: manadatory reference to this object.
        - elements: this set is populated with these elements.

        Returns:
        None
        """
        pass

    def add(self, element: Any) -> None:
        """Adds element to this set.

        element must be hashable by python.

        Args:
        - self: manadatory reference to this object.
        - element: the element to add to this set

        Returns:
        None
        """
        pass    

    def discard(self, element: Any) -> None:
        """Removes element from this set.

        there is noting to be done if element is not present in this set.

        Args:
        - self: manadatory reference to this object.
        - element: the element to remove from this set

        Returns:
        None
        """
        pass    

    def __iter__(self):
        """Makes this set iterable.

        There are many different ways to implement this. Choose one that works
        for you.

        Args:
        - self: manadatory reference to this object.
        """
        pass    

class ChainedSet(MySet):
    '''Overrides and implementes the methods defined in MySet. Uses a chained
    hash table to implement the set.
    '''
    def __init__(self, elements: [Any]) -> None:
        """Initializes this set with elements.

        Each element in elements must be hashable by python.

        Args:
        - self: manadatory reference to this object.
        - elements: this set is populated with these elements.

        Returns:
        None
        """
        self.tableLength = 1 #Empty Hash Table Length
        self.totalItems = 0  #0 Items in the Hash Table initially
        
        self.table = [[] for i in range(self.tableLength)] #Initializing the hash table with tableLength buckers

        for elem in elements: #Adding each item to the hash table and resizing appropriately
            self.add(elem)



    def add(self, element: Any) -> None:
        """Adds element to this set.

        element must be hashable by python.

        Args:
        - self: manadatory reference to this object.
        - element: the element to add to this set

        Returns:
        None
        """
        if not(self.get(element)):
            self.totalItems += 1

            # Calculate Load Factor when inserting a new element
            self.loadFactor = self.totalItems / self.tableLength

            if self.loadFactor > 0.75:
                self._resize()

            index = self._hash(element)
            self.table[index].append(element)


    def discard(self, element: Any) -> None:
        """Removes element from this set.

        there is noting to be done if element is not present in this set.

        Args:
        - self: manadatory reference to this object.
        - element: the element to remove from this set

        Returns:
        None
        """
        index = self._hash(element)

        if not(self.table[index]) and element not in self.table[index]:
            return

        else:
            for elem in self.table[index]:
                if elem == element:
                    self.table[index].remove(elem)

    def get(self, element: Any, default: Any = None) -> Any:
        index = self._hash(element)

        if not(self.table[index]) and element not in self.table[index]:
            return default

        else:
            for elem in self.table[index]:
                if elem == element:
                    return elem

    def __iter__(self):
        """Makes this set iterable.

        There are many different ways to implement this. Choose one that works
        for you.

        Args:
        - self: manadatory reference to this object.
        """
        for x in self.table:
            for y in x:
                if y != None:
                    yield y

    def _hash(self, key):
        return (hash(key) % self.tableLength)

    def _resize(self):
        self.tableLength = self.tableLength * 2

        newTable = [[] for i in range(self.tableLength)]

        for bucket in self.table:
            if bucket:
                for elem in bucket:
                    index = self._hash(elem)
                    newTable[index].append(elem) 

        self.table = newTable

class LinearSet(MySet):
    '''Overrides and implementes the methods defined in MySet. Uses a linear
    probing hash table to implement the set.
    '''
    def __init__(self, elements: [Any]) -> None:
        self.tableLength = 1
        self.totalItems = 0
        self.deleted = 0
        
        self.table = [None for i in range(self.tableLength)]

        for elem in elements:
            self.add(elem)

    def add(self, element: Any) -> None:
        if self._search(element) == None:
            self.totalItems += 1
            # Calculate Load Factor when inserting a new element
            self.loadFactor = self.totalItems / self.tableLength

            
            if self.loadFactor > 0.7 :
                self._resize()

            index = self._hash(element)
            self.table[index] = element

    def _search(self, key):
        index = (hash(key) % self.tableLength)

        while self.table[index] != None:
            if key == self.table[index] and self.table[index] != "del":  
                # print(f'crashing here ig {key} {self.table[index]}')
                return index
            index = (index + 1) % self.tableLength
            
        # print('after searching')
        return None

    def _hash(self, key):
        index = (hash(key) % self.tableLength)

        if self.table[index] == None or self.table[index] == 'del':
            return index

        while self.table[index] != None and self.table[index] != 'del':
            index = (index+1) % self.tableLength

        return index

    def _resize(self, downsize=False):
        # print('resizing')
        if downsize:
            self.totalItems -= self.deleted
            self.deleted = 0
            self.tableLength = int(self.totalItems * 2)
        else:
            self.tableLength = self.tableLength * 2

        oldTable = self.table
        self.table = [None for i in range(self.tableLength)]

        for elem in oldTable:
            if elem != None and elem != 'del':
                index = self._hash(elem)
                self.table[index] = elem

        # print('done resizing')

    def discard(self, element: Any) -> None:
        index = self._search(element)
        if index != None:
            # print(self.table)
            # print(f'index: {index}, tableSize: {self.tableLength}, elements: {self.totalItems}')
            # print()
            if self.table[index] == element and index != 'del':
                self.table[index] = 'del'
                self.deleted += 1

                # Calculate Load Factor when inserting a new element
                self.loadFactor = self.totalItems / self.tableLength

                if self.loadFactor < 0.25:
                    self._resize(True) #Downsize

    def __iter__(self):
        for x in self.table:
            if x != None and x != 'del':
                yield x 

class MyDict(object):
    '''An abstract class that provides a dictionary interface which is just
    sufficient for the implementation of this assignment.
    '''

    def __init__(self) -> None:
        """Initializes this dictionary.

        Args:
        - self: manadatory reference to this object.

        Returns:
        none
        """
        pass
    
    def __setitem__(self, key: Any, newvalue: Any) -> None:
        """Adds (key, newvalue) to the dictionary, overwriting any prior value.

        dunder method allows assignment using indexing syntax, e.g.
        d[key] = newvalue

        key must be hashable by pytohn.
        
        Args:
        - self: manadatory reference to this object.
        - key: the key to add to the dictionary
        - newvalue: the value to store for the key, overwriting any prior value 

        Returns:
        None
        """
        pass
    
    def get(self, key: Any, default: Any = None) -> Any:
        """Returns the value stored for key, default if no value exists.

        key must be hashable by pytohn.
        
        Args:
        - self: manadatory reference to this object.
        - key: the key whose value is sought.
        - default: the value to return if key does not exist in this dictionary

        Returns:
        the stored value for key, default if no such value exists.
        """
        pass

    def items(self) -> [(Any, Any)]:
        """Returns the key-value pairs of the dictionary as tuples in a list.
        
        Args:
        - self: manadatory reference to this object.

        Returns:
        the key-value pairs of the dictionary as tuples in a list.
        """
        pass

    def clear(self) -> None:
        """Clears the dictionary.

        Args:
        - self: manadatory reference to this object.

        Returns:
        None.
        """
        pass

class ChainedDict(MyDict):
    '''Overrides and implementes the methods defined in MyDict. Uses a chained
    hash table to implement the dictionary.
    '''
    def __init__(self) -> None:
        self.tableLength = 1
        self.totalItems = 0
        
        self.table = [[] for i in range(self.tableLength)]

    def __setitem__(self, key: Any, newvalue: Any) -> None:
        if not(self.get(key)):
            self.totalItems += 1

            # Calculate Load Factor when inserting a new element
            self.loadFactor = self.totalItems / self.tableLength

            if self.loadFactor > 0.75:
                # print(f'Old Length: {self.tableLength}')
                self._resize()
                # print(f'New Length: {self.tableLength}')


        index = self._hash(key)

        if not(self.get(key)):
            self.table[index].append([key, newvalue])
        else:
            for elem in range(len(self.table[index])):
                if self.table[index][elem][0] == key:
                    self.table[index][elem][1] = newvalue

    def get(self, key: Any, default: Any = 0) -> Any:
        index = self._hash(key)

        if not(self.table[index]):
            return default
        
        else:
            for elem in self.table[index]:
                if elem[0] == key:
                    return elem[1]
            return 0

    def items(self) -> [(Any, Any)]:
        items = []
        for bucket in self.table:
            for elem in bucket:
                items.append((elem[0], elem[1]))

        return items

    def clear(self) -> None:
        self.tableLength = 1
        self.totalItems = 0
        self.table = [[] for i in range(self.tableLength)]

    def _hash(self, key):
        return (hash(key) % self.tableLength)

    def _resize(self):
        self.tableLength = self.tableLength * 2

        newTable = [[] for i in range(self.tableLength)]

        for bucket in self.table:
            if bucket:
                for elem in bucket:
                    index = self._hash(elem[0])
                    newTable[index].append(elem) 

        self.table = newTable

class LinearDict(MyDict):
    '''An abstract class that provides a dictionary interface which is just
    sufficient for the implementation of this assignment.
    '''

    def __init__(self) -> None:
        self.tableLength = 1
        self.totalItems = 0
        
        self.table = [None for i in range(self.tableLength)]
    
    def __setitem__(self, key: Any, newvalue: Any) -> None:
        # Check if item already exists
        if self._search(key) == None:
            self.totalItems += 1

            # Calculate Load Factor when inserting a new element
            self.loadFactor = self.totalItems / self.tableLength

            if self.loadFactor > 0.4:
                # print(f'Old Length: {self.tableLength}')
                self._resize()
                # print(f'New Length: {self.tableLength}')

            index = self._hash(key)
            self.table[index] = [key, newvalue]
        else:
            # Find index of the existing item
            index = self._search(key)
            #update item
            self.table[index][1] = newvalue

    # Search for an item
    def _search(self, key):
        index = (hash(key) % self.tableLength)

        if self.table[index] != None:
            if self.table[index][0] == key:
                return index
            else:
                while self.table[index][0] != key:
                    index = (index + 1) % self.tableLength
                    if self.table[index] == None:
                        return None
                return index
        return None
                
    def get(self, key: Any, default: Any = None) -> Any:
        index = self._search(key)

        if index != None:
            return self.table[index][1]
        return default

    def _hash(self, key):
        index = (hash(key) % self.tableLength)

        if self.table[index] == None:
            return index

        while self.table[index] != None :
            index = (index+1) % self.tableLength

        return index

    def _resize(self):
        self.tableLength = self.tableLength * 2

        oldTable = self.table
        self.table = [None for i in range(self.tableLength)]

        for elem in oldTable:
            if elem != None:
                index = self._hash(elem[0])
                self.table[index] = elem

    def items(self) -> [(Any, Any)]:
        items = []
        for elem in self.table:
            if elem != None:
                items.append((elem[0], elem[1]))

        return items

    def clear(self) -> None:
        self.tableLength = 1
        self.totalItems = 0
        
        self.table = [None for i in range(self.tableLength)]
