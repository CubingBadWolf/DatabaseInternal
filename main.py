import tabulate
import sqlite3
import os
from SanitiseStrings import SanitiseData
from AddQueries import *
from SearchQueries import *

if not os.path.exists('Database.db'):
    os.system("python CreateDatabase.py")

conn = sqlite3.connect('Database.db')
c = conn.cursor()

def UpdateStudentINFO(StudentID):
    c.execute('''SELECT * FROM Students WHERE ID = ?;''', [StudentID])
    info = c.fetchone()
    studentinfo=[item for item in info]
    studentinfo.pop(0)

    print('Here is the original entry')
    cursor = c.execute(f"SELECT * FROM Students;")
    collumns = [description[0] for description in cursor.description]

    collumns.pop(0) # Removes the ID collumn as that will never be changed

    print(tabulate.tabulate([studentinfo], headers=collumns, tablefmt='github'))
    while True:
        updateCollumns = input('How many collumns do you wish to update?: ')
        try:
            updateCollumns = int(updateCollumns)
            if updateCollumns <0 or updateCollumns > len(collumns):
                print(f'Please enter a valid number of collumns to update (0 - {len(collumns)})')
            else:
                break
        except ValueError:
            print('Please enter a number')

    print(f'Where the collums are ordered left to right beginning at 0 ({collumns[0]} = 0 -> {collumns[-1]} = {len(collumns)-1})')
    update =[]
    for i in range(updateCollumns):
        while True:
            collumn = input('Which collumn do you want to update?:')
            try:
                collumn = int(collumn)
                if collumn < 0 or collumn > len(collumns)-1:
                    print('Please enter a valid collumn number')

                elif collumn in update:
                    print('You have already added that collumn please enter another collumn')
                else:
                    update.append(collumn)
                    break
            except ValueError:
                print('Please enter a number')

    for collumn in update:
        changed = SanitiseData(input(f'What would you like to change the {collumns[collumn]} collumn to?:'))
        c.execute(f'''UPDATE Students SET {collumns[collumn]} = ?
                    WHERE ID = {StudentID}''',[changed])
    conn.commit()
                    

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
#print(tabulate.tabulate(ClassFromTeacher(['John',"Smith"]), headers=['Class Name', 'Year Level'], tablefmt= 'github')+'\n')
#print(tabulate.tabulate(StudentsFromTeachers(['Malcolm',"Tremayne"]), headers=['First Name', 'Last Name'], tablefmt= 'github')+'\n')
#print(tabulate.tabulate(StudentsFromClassID(12), headers=['First Name', 'Last Name'],tablefmt='github'))

#AddClass('Calculus', YearLvl=None) #Works
#AddTeacher(SubjectName=None, YearLvl=None) #Works
#AddStudent() #Works
#AddTeacher('Programming',10)
UpdateStudentINFO(2)