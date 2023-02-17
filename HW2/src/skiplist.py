import random
import sys
# from turtle import update
from typing import Any, Optional

class Node(object):
    '''A node in a skiplist. It stores a (key, value) pair along with pointers
    for each level in its tower.

    The key is used to compare nodes. The tower automatically includes level 0.
    '''
    
    def __init__(self, data: (Any,Any) = None, height: int=0) -> None:
        '''Construct node with given data and of given height.

        The height is the largest level, starting from 0, of the tower.

        Parameters:
        - self: mandatory reference to this object
        - data: the (key, value) pair to store in this node
        - height: the number of levels in the tower (excludes level 0)

        Returns:
        None
        '''
        self.data = data
        self.height = height
        self.next = [None for i in range(height + 1)]

    def __repr__(self) -> str:
        '''Returns the representation of this node.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        this node's string representation.
        '''
        return repr(self.data)

    def __str__(self) -> str:
        '''Returns a string representation of this node.

        See the given link for the difference between the __repr__ and __str__
        methods: https://www.geeksforgeeks.org/str-vs-repr-in-python/

        Parameters:
        - self: mandatory reference to this object

        Returns:
        this node's string representation.
        '''
        return self.__repr__()
    
    def height(self) -> int:
        '''Returns the height of this node's tower.

        The height is the largest level, starting from 0, of the tower.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        the height of this node's tower.
        '''
        return (self.height + 1)

    def key(self) -> Any:
        '''Returns the key stored in this node.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        the key stored in this node.
        '''
        return self.data[0]

    def value(self) -> Any:
        '''Returns the value stored in this node.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        the value stored in this node.
        '''
        return self.data[1]

class SkipList(object):
    '''A skiplist of nodes containing (key, value) pairs. Nodes are ordered
    according to keys. Keys are unique, reinserting an existing key overwrites
    the value.

    The skiplist contains a sentinel node by default and the height of the
    sentinel node is the height of the list.
    '''

    def __init__(self) -> None:
        '''Construct emote skiplist.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        None
        '''
        self.head = Node()
        self.height = 0
        self.level = 0
        self.size = 0

    def __len__(self) -> int:
        '''Returns the number of pairs stored in this skiplist.

        dunder method allows calling len() on this object.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        the number of pairs stored in this skiplist.
        '''
        return self.size

    def __repr__(self) -> str:
        '''Returns a string representation of this skiplist.

        Implement any representation that helps you debug.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        this skiplist's string representation.
        '''
        return repr(self.data)
    
    def __str__(self) -> str:
        '''Returns a string representation of this skiplist.

        See the given link for the difference between the __repr__ and __str__
        methods: https://www.geeksforgeeks.org/str-vs-repr-in-python/

        Parameters:
        - self: mandatory reference to this object

        Returns:
        this skiplist's string representation.
        '''
        return self.__repr__()

    def _search_path(self, key: Any) -> [Node]:
        '''Returns the search path in this skiplist for key.

        The search path contains one node for each level of the skiplist
        starting from the highest and ending at level 0. The node for each
        level is the one corresponding to a descend in the search path.

        Parameters:
        - self: mandatory reference to this object
        - key: the key being searched for

        Returns:
        the descend nodes at each level of the skiplist, ordered from highest
        level to level 0.
        '''
        path = []
        curr = self.head

        level = self.level - 1
        while level >= 0:
            while curr.next[level] is not None and curr.next[level].data[0] <= key:
                curr = curr.next[level]
                path.append(curr.data)
            level -= 1
        if curr is not None and curr.data[0] == key:
            return path
        return None


    def _find_prev(self, key: Any) -> Node:
        '''Returns the node in the skiplist that contains the predecessor key.

        Parameters:
        - self: mandatory reference to this object
        - key: the key being searched for

        Returns:
        the node in the skiplist that contains the predecessor key.
        '''
        curr = self.head
        level = self.level - 1

        while level >= 0:
            while curr.next[level] is not None and curr.next[level].data[0] < key:
                curr = curr.next[level]
            level -= 1

        return curr

        # if curr.next[0] is not None:
        #     if curr.next[0].data[0] == key:
        #         return curr
        # return None

    def reset(self) -> None:
        '''Empty the skiplist.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        None
        '''
        self.__init__()

    def height(self) -> int:
        '''Returns the height of the skiplist.

        The height is the largest level of the sentinel's tower.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        the height of this skiplist.
        '''
        return self.level

    def find(self, key: Any) -> Optional[Any]:
        '''Returns the value stored in this skiplist corresponding to key, None
        if key does not exist in this skiplist.

        Parameters:
        - self: mandatory reference to this object
        - key: the key whose value is sought

        Returns:
        the stored value for key, None if key does not exist in this skiplist.
        '''
        curr = self._find_prev(key).next[0]
        if curr and curr.data[0] == key:
            return curr.data[1]
        else:
            return None


    def find_range(self, key1: Any, key2: Any) -> [Any]:
        '''Returns the values stored in this skiplist corresponding to the keys
        between key1 and key2 inclusive in sorted order of keys.

        Parameters:
        - self: mandatory reference to this object
        - key1: starting key in the range of keys whose value is sought
        - key2: ending key in the range of keys whose value is sought

        Returns:
        the stored values for the keys between key1 and key2 inclusive in sorted
        order of keys.
        '''
        if key2 < key1:
            return None

        curr = self._find_prev(key1).next[0]
        rangeList = []

        if curr is not None and curr.data[0] == key1:
            while curr is not None and curr.data[0] != key2:
                rangeList.append(curr.data[1])
                curr = curr.next[0]
            rangeList.append(curr.data[1])
            return rangeList
        else:
            # print('aaa not found here')
            return None

    def remove(self, key: Any) -> Optional[Any]:
        '''Returns the value stored for key in this skiplist and removes
        (key, value) from this skiplist, returns None if key is not stored in
        this skiplist.

        Parameters:
        - self: mandatory reference to this object
        - key: the key to be removed

        Returns:
        the stored value for key in this skiplist, None if key does not exist
        in this skiplist
        '''
        curr = self.head
        newList = [None for i in range(self.level)]

        level = self.level - 1
        while level >= 0:
            while curr.next[level] is not None and curr.next[level].data[0] < key:
                curr = curr.next[level]
            newList[level] = curr
            level -= 1
        curr = curr.next[0]

        if curr is not None and curr.data[0] == key:
            for h in range(self.level):
                if newList.next[h] != curr:
                    break
                newList[h].next[h] = curr.next[h]

            while self.level > 0 and self.head.next[self.level] == None:
                self.level -= 1

            return curr.data[1]
        return None

    def insert(self, data: (Any,Any)) -> None:
        '''Inserts a (key value) pair in this skiplist, overwrites the old value
        if key already exists.

        Parameters:
        - self: mandatory reference to this object
        - data: the (key, value) pair

        Returns:
        None
        '''
        curr = self.head
        height = self.genHeight()

        newHeight = max(height, self.level)
        newList = [None for i in range(newHeight)]

        level = self.level - 1
        while level >= 0:
            while curr.next[level] is not None and curr.next[level].data[0] < data[0]:
                curr = curr.next[level]
            newList[level] = curr
            # print(level)
            level -= 1
        curr = curr.next[0]

        if curr is None or curr.data[0] != data[0]:
            newNode = Node(data, height) 
            sentinalLevel = self.level
            while sentinalLevel < height:
                newList[sentinalLevel] = self.head
                self.head.next.append(None)
                sentinalLevel += 1
            
            self.level = newHeight
            for i in range(height):
                newNode.next[i] = newList[i].next[i]
                newList[i].next[i] = newNode
            self.size += 1
        else:
            curr.data = data

    def size(self) -> int:
        '''Returns the number of pairs stored in this skiplist.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        the number of pairs stored in this skiplist.
        '''
        return self.size
    
    def is_empty(self) -> bool:
        '''Returns whether the skiplist is empty.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        True if no pairs are stored in this skiplist, False otherwise.
        '''
        return True if self.head.next[0] == None else False

    def genHeight(self):
        height = 1
        while random.randint(0, 1) == 1:
            height += 1
        return height