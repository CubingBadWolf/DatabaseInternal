import os

if not os.path.exists('Database.db'):
    os.system("python CreateDatabase.py")

import tabulate
import sqlite3
from SanitiseStrings import SanitiseData
from AddQueries import *
from SearchQueries import *
from UpdateQueries import *

conn = sqlite3.connect('Database.db')
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

#printAll(getTables()) #Test functions to check database is created correctly

#print(tabulate.tabulate(ClassFromStudent(['dfdsf','fsdf']), headers=['Class Name'], tablefmt= 'github')+'\n')
#print(tabulate.tabulate(ClassFromTeacher(['John',"Smith"]), headers=['Class Name', 'Year Level'], tablefmt= 'github')+'\n')
#print(tabulate.tabulate(StudentsFromTeachers(['Malcolm',"Tremayne"]), headers=['First Name', 'Last Name'], tablefmt= 'github')+'\n')
#print(tabulate.tabulate(StudentsFromClassID(12), headers=['First Name', 'Last Name'],tablefmt='github'))

#AddClass('Science', YearLvl=10) #Works
#AddTeacher(SubjectName=None, YearLvl=None) #Works
#AddStudent() #Works
#AddTeacher('Programming',10) #Works
#UpdateStudentINFO(52) #Works

conn.close()