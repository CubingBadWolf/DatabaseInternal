import tabulate
import sqlite3
import os

if not os.path.exists('Database.db'):
    os.system("python CreateDatabase.py")

conn = sqlite3.connect('Database.db')
c = conn.cursor()

def ClassFromStudent(StudentName):
    '''Returns the classes a student takes when provided with the students name'''
    query = f'''SELECT Classes.Name
            FROM Students
            JOIN Students_Classes ON Students.ID = Students_Classes.StudentsID
            JOIN Classes ON Students_Classes.ClassesID = Classes.ID
            WHERE Students.first_name = '{StudentName[0]}' AND Students.last_name = '{StudentName[1]}';'''
    c.execute(query)
    return c.fetchall()

def ClassFromTeacher(TeacherName):
    '''Returns the classes and the class year level when given a teachers name'''
    query = f'''SELECT Classes.Name, Classes.Year_Level
            FROM Teachers
            JOIN Teachers_Classes ON Teachers.ID = Teachers_Classes.TeachersID
            JOIN Classes ON Teachers_Classes.ClassesID = Classes.ID
            WHERE Teachers.first_name = '{TeacherName[0]}' AND Teachers.last_name = '{TeacherName[1]}';'''
    c.execute(query)
    return c.fetchall()


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

print(tabulate.tabulate(ClassFromStudent(['Velma','Brissenden']), headers=['Class Name'], tablefmt= 'github'))
print(tabulate.tabulate(ClassFromTeacher(['Malcolm','Tremayne']), headers=['Class Name', 'Year Level'], tablefmt= 'github'))