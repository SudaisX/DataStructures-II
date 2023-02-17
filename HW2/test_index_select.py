import pytest
import sys
sys.path.append("./src")

from db import Table
from data import Data

datafile = "https://waqarsaleem.github.io/cs201/hw2/books.csv"

data = Data(datafile)
table = Table()
table.read('data/books.csv')

@pytest.mark.parametrize('i', range(100))
def test_select(i):
    record = data.get_random_record()
    idx = data.get_random_header_index()
    attribute = data.get_header(idx)
    table.create_index(attribute)
    key = record[idx]
    result = table.select(key)
    assert result == record, \
        f'{i+1}. FAIL: {attribute=}, {key=}.\nQuery {result=}\n{record=}'
