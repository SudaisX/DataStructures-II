from array import array

class MyList:
    '''A list interface. Also implements Iterator functions in order to support
    iteration over this list.
    '''
    def __init__(self, size: int, value=None) -> None:
        self.size = size
        self.value = value
        self.list = [self.value for i in range(self.size)]

    def __len__(self) -> int: 
        return self.size

    def __getitem__(self, i: int):
        # Ensure bounds.        
        assert 0 <= i < len(self),\
            f'Getting invalid list index {i} from list of size {len(self)}'
        
        return self.list[i]

    def __setitem__(self, i: int, value) -> None:
        # Ensure bounds.
        assert 0 <= i < len(self),\
            f'Setting invalid list index {i} in list of size {len(self)}'
        self.list[i] = value

    def __iter__(self):
        self._iter_index: int = 0 #Initialize iteration index.
        return self

    def __next__(self):
        if self._iter_index < len(self):
            value = self.get(self._iter_index)
            self._iter_index += 1
            return value
        else:
            self._iter_index = 0 
            raise StopIteration #End of Iteration

    def get(self, i: int):
        return self[i]

    def set(self, i: int, value) -> None:
        self[i] = value

class ArrayList(MyList): 
    def __init__(self, size: int, value=(0,0,0)) -> None:
        self.size = size

        self.arr_red = array("i",[value[0] for i in range(size)])
        self.arr_green = array("i",[value[1] for i in range(size)])
        self.arr_blue = array("i",[value[2] for i in range(size)])

    def __len__(self):
        return self.size

    def __getitem__(self, i: int):
        return (self.arr_red[i], self.arr_green[i], self.arr_blue[i])

    def __setitem__(self, i: int, itemValue):
        self.arr_red[i] = itemValue[0]
        self.arr_green[i] = itemValue[1]
        self.arr_blue[i] = itemValue[2]

        # print(self[i], end=' = ')
        # print(itemValue)

class Node:
    def __init__(self, value=None):
        self.value=value
        self.next=None

class PointerList(MyList):
    def __init__(self, size: int, value=None) -> None:
        self.size = size
        self.head = Node(value)
        
        curr = self.head
        for i in range(size):
            curr.next = Node(value)
            curr = curr.next

    def __len__(self): 
        return self.size

    def __getitem__(self, i: int):
        # Ensure bounds.        
        assert 0 <= i < len(self),\
            f'Getting invalid list index {i} from list of size {len(self)}'
        
        currIndex = 0
        curr = self.head
        while curr.next != None:
            if currIndex == i:
                return curr.value
                
            currIndex += 1
            curr = curr.next

    def __setitem__(self, i: int, value) -> None:
        # Ensure bounds.
        assert 0 <= i < len(self),\
            f'Setting invalid list index {i} in list of size {len(self)}'
        
        currIndex = 0
        curr = self.head
        while curr.next != None:
            if currIndex == i:
                curr.value = value
                break
                
            currIndex += 1
            curr = curr.next

    def __iter__(self):
        self._iter_index: int = 0 #Initialize iteration index.
        return self

    def __next__(self):
        if self._iter_index < len(self):
            value = self.get(self._iter_index)
            self._iter_index += 1
            return value
        else:
            self._iter_index = 0 
            raise StopIteration #End of Iteration

    def get(self, i: int):
        return self[i]

    def set(self, i: int, value) -> None:
        # print(self[i], end=' = ')
        # print(value)
        self[i] = value
