import os
from CreateDatabase import MakeDB
if not os.path.exists('Database.db'):
    MakeDB()
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

#print(tabulate.tabulate(ClassFromStudent(['Velma','Brissenden']), headers=['Class Name'], tablefmt= 'github')+'\n')
print(tabulate.tabulate(ClassFromTeacher(['Mary',"Kienzle"]), headers=['Class Name', 'Year Level'], tablefmt= 'github')+'\n')
#print(tabulate.tabulate(StudentsFromTeachers(['Malcolm',"Tremayne"]), headers=['First Name', 'Last Name'], tablefmt= 'github')+'\n')
#print(tabulate.tabulate(StudentsFromClassID(12), headers=['First Name', 'Last Name'],tablefmt='github'))

#AddClass('Science', YearLvl=10) #Works
#AddTeacher(SubjectName=None, YearLvl=None) #Works
#AddStudent() #Works
#AddTeacher('Programming',10) #Works
#UpdateStudentINFO(conn, 2) #Works
UpdateTeacherINFO(conn, 2)
conn.close()