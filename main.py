import tabulate
import sqlite3
from CreateDatabase import BuildDB

BuildDB()

conn = sqlite3.connect('Test.db')
c = conn.cursor()

def getTables():
    '''Returns the names of all tables in the database'''
    c.execute("SELECT name FROM sqlite_schema WHERE type= 'table' AND name NOT LIKE 'sqlite_%';")
    return c.fetchall()

def printAll(tables):
    '''Takes the tables in the database and returns all the tables and data'''
    for table in tables:
        cursor = c.execute(f"SELECT * FROM {table[0]};")
        collums = [description[0] for description in cursor.description]

        c.execute(f"SELECT * FROM {table[0]};")
        print(tabulate.tabulate(c.fetchall(), headers=collums, tablefmt='github'))
        print('')

printAll(getTables()) #Test functions to check database is created correctly