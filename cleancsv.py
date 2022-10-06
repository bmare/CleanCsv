import csv, sys, os, io, re, json

import psycopg2

from contextlib import contextmanager
from datetime import datetime, time
from typing import Iterator, Optional

from definitions import ROOT_DIR, JSON_DIR

@contextmanager
def open_db():
    """
    Supplies a cursor for database transactions.
    Usage: with open_db() as curs:
    :yields curs
    """
    conn = psycopg2.connect(user='postgres', password='', host='localhost', port='5432', database='testload')
    try:
        curs = conn.cursor()
        yield curs
    except Exception as error:
        print(error)
    finally:
        conn.commit()
        conn.close()

def get_conn():
    return psycopg2.connect(user='postgres', password='***REMOVED***', host='localhost', port='5432', database='eoir_foia')

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


class CleanCsv:
    def __init__(self, csvfile) -> None:
        """
        Set variables with filepaths
        """
        self.csvfile = csvfile
        self.header = self.get_header()
        self.header_length = len(self.header)
        self.name = os.path.basename(self.csvfile)
        self.js_name = f"{JSON_DIR}/{self.name.replace('.csv', '.json')}"
        self.no_nul = os.path.abspath(self.csvfile).replace('.csv', '_no_nul.csv')
        self.bad_row = os.path.abspath(self.csvfile).replace('.csv', '_br.csv')
        try:
            with open(f"{JSON_DIR}/tables.json", 'r') as f:
                self.table = json.load(f)[self.name]
            with open(f"{JSON_DIR}/table-dtypes/{os.path.basename(self.js_name)}", 'r') as f:
                self.dtypes = json.load(f)
        except FileNotFoundError as e:
            print(f"Need to setup json file for table. {e}")

    def copy_to_table(self, table='') -> None:
        """
        iter_csv uses StringIteratorIO to create a file-like object from the generator csv_gen().
        """
        with open_db() as curs:
            if not table:
                table = self.table
            iter_csv = StringIteratorIO(iter(self.csv_gen()))
            curs.copy_from(iter_csv, table, sep='|', null='\\N', size=8192)


    def replace_nul(self) -> None:
        """
        Replace nul bytes in csv file. Write to self.no_nul
        """
        fi = open(self.csvfile, 'rb')
        data = fi.read()
        fi.close()
        fo = open(self.no_nul, "wb")
        fo.write(data.replace(b'\x00', b''))
        fo.close()

    def del_no_nul(self) -> None:
        """
        Delete the no_nul file
        """
        os.remove(self.no_nul)
    

    def csv_gen(self) -> list:
        """
        Create a generator from csv file that yields cleaned and formatted rows. 
        This is where handling of short or long rows are handled. Rows are added
        to short rows. Rows are removed from long rows if they are empty. If extra
        columns in long rows are not empty, the program attempts to remove values
        that would align the rows to the data types specified in the dtype file.
        """
        with open(self.no_nul, 'r', newline='', encoding='utf-8', errors='replace') as f:
            for i, row in enumerate(csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)):
                if i == 0:
                    continue # skip header row
                elif len(row) > self.header_length:
                    clean_extra = self.remove_extra_cols(row)
                    if clean_extra:
                        yield self.clean_row(clean_extra)
                    else:
                        continue # [TODO] Fix bad header
                elif len(row) == self.header_length:
                    yield self.clean_row(row)
                elif len(row) < self.header_length:
                    yield self.clean_row(self.add_extra_cols(row))

    def get_bad_rows(self) -> list:
        """
        Create a generator from csv file that yields cleaned and formatted rows. 
        This is where handling of short or long rows are handled. Rows are added
        to short rows. Rows are removed from long rows if they are empty. If extra
        columns in long rows are not empty, the program attempts to remove values
        that would align the rows to the data types specified in the dtype file.
        """
        bad_rows = []
        with open(self.no_nul, 'r', newline='', encoding='utf-8', errors='replace') as f:
            for i, row in enumerate(csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)):
                if i == 0:
                    continue # skip header row
                elif len(row) > self.header_length:
                    bad_rows.append(row)
                    # clean_extra = self.remove_extra_cols(row)
                    # if clean_extra:
                    #     yield self.clean_row(clean_extra)
                    # else:
                    #     continue
                    #     # continue # [TODO] Fix bad header
                elif len(row) == self.header_length:
                    # yield self.clean_row(row)
                    pass
                elif len(row) < self.header_length:
                    # yield self.clean_row(self.add_extra_cols(row))
                    pass

        with get_reader_writer(self.bad_row, 'w') as w:
            for row in bad_rows:
                w.writerow(row)



    def clean_row(self, row) -> str:
        """
        Iterate over the row and check that values are the correct datatype, otherwise convert to null 
        """
        for i, value in enumerate(row):
            dtype = list(self.dtypes.values())[i] # Gets the column datatype (json file name, regex, integer,timestamp, time or text)
            value = value.strip('\\').strip()
            if self.is_nul_like(value):
                row[i] = r'\N'
                continue
            elif dtype == 'timestamp without time zone':
                row[i] = self.convert_timestamp(value)
                continue
            elif dtype == 'time without time zone':
                row[i] = self.convert_time(value)
                continue
            elif dtype == 'integer':
                row[i] = self.convert_integer(value)
                continue
            else:
                row[i] = value
        return '|'.join(row) + '\n'

    def get_bad_values(self,row) -> list[(int, str)]:
        """
        The first step in cleaning a row with shifted data. Map the bad values.
        """
        bad_values = []
        codes = self.get_codes()
        for i, value in enumerate(row):
            try:
                dtype = list(self.dtypes.values())[i] # Gets the column datatype (json file name, regex, integer,timestamp, time or text)
                value = value.strip('\\').strip()
                if self.is_nul_like(value):
                    continue
                elif dtype[0] == '^': #dtype is a regex
                    if not re.match(dtype, value):
                        bad_values.append((i, value))
                elif dtype.endswith('.json'):
                    if value not in codes[dtype].keys(): # see if value is in lookups
                        bad_values.append((i, value))
                elif dtype == 'timestamp without time zone':
                    if self.convert_timestamp(value) == r'\N':
                        bad_values.append((i, value))
                elif dtype == 'time without time zone':
                    if self.convert_time(value) == r'\N':
                        bad_values.append((i, value))
                elif dtype == 'integer':
                    if self.convert_integer(value) == r'\N': 
                        bad_values.append((i, value))
                else:
                    continue
            except IndexError:
                # import IPython; IPython.embed()
                return bad_values

    def shift_values(self, row):
        """
        Certain bad values can be removed. E.g. '\x07' row.remove('\x07')
        Other bad rows each value needs to be checked to see if it belongs in another column.
        """
        bad_vals = self.get_bad_values(row)
        for bv in bad_vals:
            row_copy = row[:] #deep copy of row 
            ix = bv[0]
            for i in range(ix,0,-1):
                if self.is_nul_like(row[i]):
                    row_copy.pop(i)
                if not self.get_bad_values(row_copy):
                    return row_copy
                else:
                    pass
                    # try:
                    #     self.shift_values(row_copy)
                    # except RecursionError:
                    #     break
            

    def remove_extra_cols(self, row) -> list:
        """
        If the extra columns are blank, remove them, otherwise return none.
        """
        extra_cols = row[self.header_length:]
        for value in extra_cols:
            if not self.is_nul_like:
                return None
        return row[:self.header_length]

    def add_extra_cols(self, row) -> list:
        """
        Append null values to short rows.
        """
        for i in range(self.header_length - len(row)):
            row.append('')
        return row

    @staticmethod
    def is_nul_like(value:str) -> bool:
        """
        Test if value should be converted to Nul
        Removes values which don't convey any meaning.
        """
        nul_like = set(['', 'b6', 'N/A', 'A.2.a'])
        if value in nul_like: 
            return True
        elif value.isspace():
            return True
        elif value[0] == '?' and value == len(value) * value[0]:
            return True
        elif value[0] == '0' and value == len(value) * value[0]:
            return True
        else:
            return False

    @staticmethod
    def convert_integer(value: str) -> str:
        """
        Test if value is convertible to an integer, if not return null
        """
        try:
            value = value.replace('O','0')
            int(value)
            return value
        except ValueError:
            return r'\N' 

    @staticmethod
    def convert_timestamp(value: str) -> str:
        """
        Test if value is convertible to an timestamp, if not return null
        """
        try:
            datetime.fromisoformat(value)
            return value
        except ValueError:
            return r'\N' 

    @staticmethod
    def convert_time(value: str) -> str:
        """
        Test if value is convertible to a time, if not return null
        """
        try:
            time.fromisoformat(value[:2] + ':' + value[2:]) 
            return value
        except ValueError:
            return r'\N' 


    def get_bad_line(self, lineno='') -> list:
        """
        When PostgreSQL copy_from fails, it may give helpful context on the line that failed.
        You can use the first value in that bad row as the lineno to look up a bad line
        """
        with open(self.no_nul, 'r', newline='', encoding='utf-8', errors='replace') as f:
            for i, row in enumerate(csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)):
                if row[0] == lineno:
                    return row

    def lookup_strange_value(self, value='') -> list:
        """
        """
        with open(self.no_nul, 'r', newline='', encoding='utf-8', errors='replace') as f:
            count = 0
            for i, row in enumerate(csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)):
                if value in row:
                    count+=1
                    print(row)
            print(f"Byte '{value}' appeared in {count} rows.")


    def get_codes(self) -> dict:
        """
        Facilitates looking up the full description for codes in the database. E.g., 'MX' -> 'Mexico'
        Get a dictionary with json filename as key, and a code: description dictionary as the value
        """
        json_files = [file for file in self.dtypes.values() if file.endswith('.json')]
        json_dicts = []
        for file in json_files:
            with open(f"{JSON_DIR}/lookups/{file}", 'r') as f:
                json_dicts.append(json.load(f))
        return dict(zip(json_files, json_dicts))


    def generate_table_type_file(self) -> None:
        """
        Facilitates the creation of a .json file with csv headers as key, and data type as value.
        Data type can be integer, time without tiemzone, timestamp without time zone, regular expression, or a codes.json file
        """
        with open(self.js_name, 'w', encoding='utf-8') as f:
            json.dump(dict(zip(self.header,[''] * self.header_length)), f, ensure_ascii=False, indent=4)


    def get_header(self) -> list:
        """
        Return first line of csv file
        """
        with get_reader_writer(self.csvfile, 'r') as r:
            return next(r)


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
