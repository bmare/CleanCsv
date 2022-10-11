import csv, sys, os, io, re, json
from typing import Iterator, Optional
from contextlib import contextmanager

import psycopg2

@contextmanager
def open_db(conn:psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
    """
    Supplies a cursor for database transactions.
    Usage: with open_db() as curs:
    :yields curs
    """
    try:
        curs = conn.cursor()
        yield curs
    except Exception as error:
        print(error)
    finally:
        conn.commit()
        conn.close()

@contextmanager
def get_reader_writer(file, rw:str):
    """
    Yield csv reader or writer given filepath and read or write string.
    """
    try:
        if rw == 'r':
            with open(file, 'r', newline='', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f, delimiter='\t', dialect='excel-tab', quoting=csv.QUOTE_NONE, escapechar='\\')
                yield reader
        elif rw == 'w':
            with open(file, 'a', newline='', encoding='utf-8', errors='replace') as f:
                writer = csv.writer(f, delimiter='\t', dialect='excel-tab', quoting=csv.QUOTE_NONE, escapechar='\\')
                yield writer
    except csv.Error as e:
        sys.exit(f"file, line {reader.line_num}, {e}")

class StringIteratorIO(io.TextIOBase):
    """
    Inherits TextIOBase, reimplementing read method to create a buffer for the text stream.
    """
    def __init__(self, iter: Iterator[str]):
        self._iter = iter
        self._buff = ''

    def readable(self) -> bool:
        return True

    def _read1(self, n: Optional[int] = None) -> str:
        while not self._buff:
            try:
                self._buff = next(self._iter)
            except StopIteration:
                break
        ret = self._buff[:n]
        self._buff = self._buff[len(ret):]
        return ret

    def read(self, n: Optional[int] = None) -> str:
        line = []
        if n is None or n < 0:
            while True:
                m = self._read1()
                if not m:
                    break
                line.append(m)
        else:
            while n > 0:
                m = self._read1(n)
                if not m:
                    break
                n -= len(m)
                line.append(m)
        return ''.join(line)

# https://pythontutor.com/render.html#code=import%20io%0A%0Aclass%20StringIteratorIO%28io.TextIOBase%29%3A%0A%20%20%20%20def%20__init__%28self,%20iter%29%3A%0A%20%20%20%20%20%20%20%20self._iter%20%3D%20iter%0A%20%20%20%20%20%20%20%20self._buff%20%3D%20''%0A%0A%20%20%20%20def%20readable%28self%29%20-%3E%20bool%3A%0A%20%20%20%20%20%20%20%20return%20True%0A%0A%20%20%20%20def%20_read1%28self,%20n%3D%20None%29%20-%3E%20str%3A%0A%20%20%20%20%20%20%20%20while%20not%20self._buff%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20try%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20self._buff%20%3D%20next%28self._iter%29%0A%20%20%20%20%20%20%20%20%20%20%20%20except%20StopIteration%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20break%0A%20%20%20%20%20%20%20%20ret%20%3D%20self._buff%5B%3An%5D%0A%20%20%20%20%20%20%20%20self._buff%20%3D%20self._buff%5Blen%28ret%29%3A%5D%0A%20%20%20%20%20%20%20%20return%20ret%0A%0A%20%20%20%20def%20read%28self,%20n%20%3D%20None%29%20-%3E%20str%3A%0A%20%20%20%20%20%20%20%20line%20%3D%20%5B%5D%0A%20%20%20%20%20%20%20%20if%20n%20is%20None%20or%20n%20%3C%200%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20while%20True%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20m%20%3D%20self._read1%28%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20if%20not%20m%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20break%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20line.append%28m%29%0A%20%20%20%20%20%20%20%20else%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20while%20n%20%3E%200%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20m%20%3D%20self._read1%28n%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20if%20not%20m%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20break%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20n%20-%3D%20len%28m%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20line.append%28m%29%0A%20%20%20%20%20%20%20%20return%20''.join%28line%29%0A%0Astr1%20%3D%20'5632%7CMX%7CES%7C%5C%5CN%7CGWT%5Cn'%0Agen%20%3D%20%28str1%20for%20i%20in%20range%283%29%29%0A%0Af%20%3D%20StringIteratorIO%28gen%29%0Aprint%28f.read%28%29%29&cumulative=false&curInstr=77&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D&textReferences=false
