import sqlite3

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

def StudentsFromTeachers(TeacherName):
    '''Returns all the students a given a teachers name'''
    query = f'''SELECT Students.first_name, Students.last_name
            FROM Classes
            JOIN Students_Classes ON Classes.ID = Students_Classes.ClassesID
            JOIN Students ON Students_Classes.StudentsID = Students.ID
            JOIN Teachers_Classes ON Classes.ID = Teachers_Classes.ClassesID
            JOIN Teachers ON Teachers_Classes.TeachersID = Teachers.ID
            WHERE Teachers.first_name = '{TeacherName[0]}' AND Teachers.last_name = '{TeacherName[1]}';'''
    c.execute(query)
    return c.fetchall()

def StudentsFromClassID(ClassID):
    query = f'''SELECT Students.first_name, Students.last_name
            FROM Classes
            JOIN Students_Classes ON Classes.ID = Students_Classes.ClassesID
            JOIN Students ON Students_Classes.StudentsID = Students.ID
            Where Classes.ID = '{ClassID}';'''
    c.execute(query)
    return c.fetchall()
