# CleanCsv
A cli tool to optimize loading dirty csv files into a postgresql databse.

## Relieve CSV Pain
Dirty data is painful to load into a database. Often times data exported from another database has undesireable bytes, rows have too many or too few columns, text appears in a date column, etc. These issues make it less than trivial to load data into a databse where every column must have a certain datatype. PostgreSQL's copy command is magical, but only when the data is clean. When the data is dirty this tool feels less than helpful.

There are many great tools out there that could deal with this problem, but they often involve loading the csv data into memory, cleaning it, and then writing that cleaned data to the database. CleanCsv aims to overcome this problem by streaming the csv data into the database. The program reads csv data into a buffer, cleans it, and copies it to the database, all the while using no memory. This is especially great for remote servers, where memory resources may be especially scarce.

## Usage
So you've obtained a csv file of some cool data you'd like to load into a database, great! CleanCsv hopes to get this data into the database as quickly as possible. To do that we need to take the following steps:
1. Create a scheam for the table we will load our data into
2. Identify the datatypes of each column
3. Clean the data
4. Copy it to the database

Load the data into a csv file
```python
cleaned_data = CleanCsv('mycsvfile.csv')
```
Now, what we want to do is take the headers from the file, create a schema for our database table, identify the datatypes of each column, clean the data
