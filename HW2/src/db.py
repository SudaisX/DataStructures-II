import csv
from typing import List, Optional
from skiplist import SkipList

class Table(object):
    '''A table that stores records and allows creation of an index on the
    records according to the values of a specified attribute. The index is used
    to efficiently retrieve records using key values. The index can be
    re-initialized in run-time using a different attribute.
    '''
    def __init__(self) -> None:
        '''Initialize this table with an empty index.

        The index is initialized with an empty skiplist.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        None
        '''
        self.data = []
        self.index = SkipList()

    def read(self, csvfile: str) -> None:
        '''Read and store records from the given CSV file.

        Parameters:
        - self: mandatory reference to this object
        - csvfile: path to a csv file that contains the records

        Returns:
        None
        '''

        with open(csvfile, encoding="utf8") as f:
            self.data = [row for row in csv.reader(f)]
        self.data = self.data[1:]

    def create_index(self, attribute: str) -> None:
        '''Construct an index using values of the specified attribute.

        attribute must be one of the column headers from the CSV file from which
        the records were read. all values for attribute must be unique.

        Any existing index is lost and a new one is constructed. The constructed
        index is empty if no records are currently stored.

        The index stores (key, value) pairs where the keys are the values of
        attribute. The value is the location, e.g. index, of the corresponding
        record. Note that the value is not the record itself.

        Parameters:
        - self: mandatory reference to this object
        - attribute: the attribute whose values are to be the keys in the index

        Returns:
        None
        '''
        self.index = SkipList()
        n = 0

        #Book Code,Title,Category,Price,Pages
        if attribute == "Book Code":
            n = 0
        elif attribute == "Title":
            n = 1
        elif attribute == "Category":
            n = 2
        elif attribute == "Price":
            n = 3
        elif attribute == "Pages":
            n = 4

        for i in range(len(self.data)):
            self.index.insert((self.data[i][n], i))

    def select(self, key: str) -> Optional[List[str]]:
        '''Return the record corresponding to the given key, None in case of
        error.

        The index is used to find the record. An error occurs if the index is
        not yet created or the key in invalid. This is indicated by a return of
        None.

        Parameters:
        - self: mandatory reference to this object
        - key: the key whose corresponding value is sought

        Returns:
        The record corresponding to key, None in case of error.
        '''
        key = self.index.find(key)

        return self.data[key] if key else None

    def select_range(self, fromKey: str, toKey: str) -> Optional[List[List[str]]]:
        '''Returns the records corresponding to the keys in the range
        [from,to] inclusive, None in case of error.

        An error occurs if no index has been created, from and to are not valid
        keys in the index, or from is not less than to.

        Parameters:
        - self: mandatory reference to this object
        - from: the starting key value in the range of keys
        - to: the ending key value in the range of keys

        Returns:
        The records in the order of the keys in the range [from,to], None in
        case of error.
        '''
        rangeList = self.index.find_range(fromKey, toKey)

        if rangeList:
            lst = [self.data[i] for i in rangeList]
        return lst

    def delete(self, key: str) -> Optional[List[str]]:
        '''Deletes the record corresponding to key from the table and the index.
        Returns the deleted record, None in case of error.

        An error occurs if no index has been created, or key does not exist in
        it.

        Parameters:
        - self: mandatory reference to this object
        - from: the starting key value in the range of keys
        - to: the ending key value in the range of keys

        Returns:
        The deleted record,  None in case of error.
        '''
        recordKey = self.index.remove(key)
        return self.data[recordKey]
