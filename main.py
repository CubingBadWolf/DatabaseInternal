import tabulate
import sqlite3
import os
from SanitiseStrings import SanitiseData

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

def AddClass(SubjectName, YearLvl):
    if SubjectName == None:
        SubjectName = SanitiseData(input('Enter what subject is being added: '))
    else:
        if YearLvl == None:
            while True:
                YearLvl = input("Enter the subject's year level: ")
                if YearLvl != '10' and YearLvl != '9':
                    print('Please enter either 10 or 9')
                else:
                    break
    c.execute('''INSERT INTO Classes VALUES (NULL, ?,?);''',[SubjectName,int(YearLvl)])
    conn.commit()

def AddTeacher(SubjectName, YearLvl):
    TeacherName = SanitiseData(input('What is the teachers full name?: ')).split()
    c.execute('''INSERT INTO Teachers Values (NULL, ?,?)''', TeacherName) # Adds the teacher to the database and assigns ID
    c.execute('''SELECT last_insert_rowid()''')
    teacherID = c.fetchone()

    while True:
        amn = input('How many classes do they teach?')
        try:
            amn = int(amn)
            if amn < 1:
                print('Please enter a positive integer')
            else:
                break
        except:
            print('Please enter a positive integer')

    for i in range(amn):
        if SubjectName == None:
            SubjectName = SanitiseData(input('Enter what subject they teach?: ')) 

        c.execute('''SELECT ID FROM Classes
                 WHERE Name = ?;''', [SubjectName])
        classes = c.fetchall()

        taken_classes = []
        for item in classes:
            c.execute('''SELECT ClassesID FROM Teachers_Classes
                     WHERE ClassesID = ?;''', item)
            taken_classes.append(c.fetchone())

        available = []
        for result in classes:
            if result not in taken_classes:
                available.append(result)# Checks for whether subject is already taught by teacher


        if len(available) == 0:
            AddClass(SubjectName, YearLvl)
            # Create a new class and add into the joining table
            c.execute('''SELECT last_insert_rowid()''')
            classID = c.fetchone()
            c.execute('''INSERT INTO Teachers_Classes VALUES (?,?);''', (int(teacherID[0]), int(classID[0]))) 

        else:
            c.execute('''INSERT INTO Teachers_Classes VALUES (?,?);''', int(teacherID[0]), int(available[0]))    #If exists create a new class.
    
    conn.commit()

def AddStudent():
    StudentName = SanitiseData(input('What is the students full name?: ')).split()
    while True:
            YearLvl = input("Enter the student's year level: ")
            if YearLvl != '10' and YearLvl != '9':
                print('Please enter either 10 or 9')
            else:
                break

    c.execute('''INSERT INTO Students Values (NULL, ?,?,?)''', (StudentName[0], StudentName[1], int(YearLvl))) # Adds the Student to the database and assigns ID
    c.execute('''SELECT last_insert_rowid()''')
    StudentID = c.fetchone()

    while True:
        amn = input('How many classes do they take?')
        try:
            amn = int(amn)
            if amn < 1:
                print('Please enter a positive integer')
            else:
                break
        except:
            print('Please enter a positive integer')

    for i in range(amn):
        SubjectName = SanitiseData(input('Enter what subject do they take?: ')) 
        c.execute('''SELECT ID FROM Classes
                 WHERE Name = ?;''', [SubjectName])
        classes = c.fetchall()
        
        if len(classes) == 0: # If Class doesn't exist

            print('You will need to create this class and add the teacher who teachers it')
            AddTeacher(SubjectName, YearLvl)
            # Create a new class and add into the joining table
            c.execute('''SELECT last_insert_rowid()''')
            classID = c.fetchone()
            c.execute('''INSERT INTO Students_Classes VALUES (?,?);''', (int(StudentID[0]), int(classID[0]))) 

        else:
            c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl])
            ClassIDs = c.fetchall()
            studentNumbers = []
            for Class in ClassIDs:
                c.execute(''' SELECT StudentsID from Students_Classes WHERE ClassesID = ?''', Class) #Returns the student's ID who take a class
                studentNumbers.append((Class, len(c.fetchall())))

            studentNumbers = sorted(studentNumbers, key=lambda x: x[0]) # Sorts the list of class numbers ascending
            print(StudentID[0], studentNumbers[0][1])
            c.execute('''INSERT INTO Students_Classes VALUES (?,?);''', [int(StudentID[0]), int(studentNumbers[0][1])]) # Adds the student to the lowest class
    
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

#AddClass('Calculus') #Works
#AddTeacher() #Works
AddStudent() #Works