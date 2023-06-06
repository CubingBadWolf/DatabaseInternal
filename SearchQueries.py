import sqlite3
from SanitiseStrings import SanitiseData

conn = sqlite3.connect('Database.db')
c = conn.cursor()

def ClassFromStudent(StudentName):
    if StudentName == None:
        StudentName = SanitiseData(input('What is the students full name?: ')).split()
        if len(StudentName) != 2:
                print(f'{StudentName} can\'t automatically be split into first and last name')
                StudentFirstName = SanitiseData(input('Please enter the first name/names: '))
                StudentLastName = SanitiseData(input('Please enter the last name/names: '))
                StudentName = [StudentFirstName, StudentLastName]
    
    '''Returns the classes a student takes when provided with the students name'''
    query = f'''SELECT Classes.Name, Classes.Year_Level
            FROM Students
            JOIN Students_Classes ON Students.ID = Students_Classes.StudentsID
            JOIN Classes ON Students_Classes.ClassesID = Classes.ID
            WHERE Students.first_name = '{StudentName[0]}' AND Students.last_name = '{StudentName[1]}';'''
    c.execute(query)
    return c.fetchall()

def ClassFromTeacher(TeacherName):
    '''Returns the classes and the class year level when given a teachers name'''
    if TeacherName == None:
        TeacherName = SanitiseData(input('What is the teachers full name?: ')).split()
        if len(TeacherName) != 2:
            print(f'{TeacherName} can\'t automatically be split into first and last name')
            TeacherFirstName = SanitiseData(input('Please enter the first name/names: '))
            TeacherLastName = SanitiseData(input('Please enter the last name/names: '))
            TeacherName = [TeacherFirstName, TeacherLastName]

    query = f'''SELECT Classes.Name, Classes.Year_Level
            FROM Teachers
            JOIN Teachers_Classes ON Teachers.ID = Teachers_Classes.TeachersID
            JOIN Classes ON Teachers_Classes.ClassesID = Classes.ID
            WHERE Teachers.first_name = '{TeacherName[0]}' AND Teachers.last_name = '{TeacherName[1]}';'''
    c.execute(query)
    return c.fetchall()

def StudentsFromTeachers(TeacherName):
    '''Returns all the students a given a teachers name'''
    if TeacherName == None:
        TeacherName = SanitiseData(input('What is the teachers full name?: ')).split()
        if len(TeacherName) != 2:
            print(f'{TeacherName} can\'t automatically be split into first and last name')
            TeacherFirstName = SanitiseData(input('Please enter the first name/names: '))
            TeacherLastName = SanitiseData(input('Please enter the last name/names: '))
            TeacherName = [TeacherFirstName, TeacherLastName]

    query = f'''SELECT Students.first_name, Students.last_name, Students.Year_Level
            FROM Classes
            JOIN Students_Classes ON Classes.ID = Students_Classes.ClassesID
            JOIN Students ON Students_Classes.StudentsID = Students.ID
            JOIN Teachers_Classes ON Classes.ID = Teachers_Classes.ClassesID
            JOIN Teachers ON Teachers_Classes.TeachersID = Teachers.ID
            WHERE Teachers.first_name = '{TeacherName[0]}' AND Teachers.last_name = '{TeacherName[1]}';'''
    c.execute(query)
    return c.fetchall()

def StudentsFromClass(ClassID):
    if ClassID == None:
        while True:
            try: 
                ClassID = int(input("Enter the class's ID: "))
                break
            except:
                print('Please enter a valid number')
                
    query = f'''SELECT Students.first_name, Students.last_name, Students.Year_Level
            FROM Classes
            JOIN Students_Classes ON Classes.ID = Students_Classes.ClassesID
            JOIN Students ON Students_Classes.StudentsID = Students.ID
            Where Classes.ID = '{ClassID}';'''
    c.execute(query)
    return c.fetchall()

def TeachersFromStudent(StudentID):
    if StudentID == None:
        while True:
            try: 
                StudentID = int(input("Enter the Student's ID: "))
                break
            except:
                print('Please enter a valid number')
                
    query = f'''SELECT Teachers.first_name, Teachers.last_name
            FROM Classes
            JOIN Students_Classes ON Classes.ID = Students_Classes.ClassesID
            JOIN Students ON Students_Classes.StudentsID = Students.ID
            JOIN Teachers_Classes ON Classes.ID = Teachers_Classes.ClassesID
            JOIN Teachers ON Teachers_Classes.TeachersID = Teachers.ID
            Where Students.ID = '{StudentID}';'''
    c.execute(query)
    return c.fetchall()
    
def TeacherFromClass(ClassID):
    if ClassID == None:
        while True:
            try: 
                ClassID = int(input("Enter the class's ID: "))
                break
            except:
                print('Please enter a valid number')

    query = f'''SELECT Teachers.first_name, Teachers.last_name
            FROM Classes
            JOIN Teachers_Classes ON Classes.ID = Teachers_Classes.ClassesID
            JOIN Teachers ON Teachers_Classes.TeachersID = Teachers.ID
            Where Classes.ID = '{ClassID}';'''
    c.execute(query)
    return c.fetchall()

def AllStudents():
    c.execute('''SELECT First_Name, Last_Name, Year_Level FROM Students;''')
    return c.fetchall()

def AllTeachers():
    c.execute('''SELECT First_Name, Last_Name FROM Teachers;''')
    return c.fetchall()

def AllClasses():
    c.execute('''SELECT Name, Year_Level FROM Classes;''')
    return c.fetchall()