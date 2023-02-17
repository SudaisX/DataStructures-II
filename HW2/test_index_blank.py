import pytest
import sys
sys.path.append("./src")

from db import Table
from data import Data

datafile = "https://waqarsaleem.github.io/cs201/hw2/books.csv"

data = Data(datafile)
table = Table()
table.read('data/books.csv')

@pytest.mark.parametrize('i', range(20))
def test_blank_index(i):
    record = data.get_random_record()
    idx = data.get_random_header_index()
    key = record[idx]
    assert table.select(key) == None, \
        f'FAIL: Select {key=} is non-None without index'
