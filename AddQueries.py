import sqlite3
import tabulate
from SanitiseStrings import SanitiseData


def AddClass(conn, SubjectName, YearLvl, teacherCreated):
    c = conn.cursor()
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
    if teacherCreated == False:
        while True:
            yn = input('Do you want to add a teacher to this class? y/n:')
            if yn.lower() == 'y':
                c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', [SubjectName,int(YearLvl)])
                newID = c.fetchone()[0]
                c.execute('''SELECT ID, first_name, last_name from Teachers;''')
                output = c.fetchall()
                ids = [str(item[0]) for item in output]
                print('Here are all the teachers')
                print(tabulate.tabulate(output, headers=['ID','First Name', 'Last Name']))
                while True:
                    teacher = input("Enter the ID of the teacher to add OR enter new to create a new teacher: ")
                    if teacher.lower() == 'new':
                        AddTeacher(conn, SubjectName, int(YearLvl))
                        break
                    else:
                        if teacher not in ids:
                            print('Please enter a valid id')
                        else:
                            c.execute('''INSERT INTO Teachers_Classes VALUES (?,?);''', [int(teacher), int(newID)]) #No risk of error because prechecked items
                            break
                break
            elif yn.lower() == 'n':
                break
            else:
                print('Please enter y or n')

    print('Addition of Class successful')
    conn.commit()

def AddTeacher(conn, SubjectName, YearLvl):
    c = conn.cursor()
    TeacherName = SanitiseData(input('What is the teachers full name?: ')).split()
    if len(TeacherName) != 2:
        print(f'{TeacherName} can\'t automatically be split into first and last name')
        TeacherFirstName = SanitiseData(input('Please enter the first name/names: '))
        TeacherLastName = SanitiseData(input('Please enter the last name/names: '))
        TeacherName = [TeacherFirstName, TeacherLastName]

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
            if YearLvl == None:
                while True:
                    YearLvl = input('What year level is this class?')
                    if YearLvl != '9' and YearLvl != '10':
                        print('Please enter 9 or 10')
                    else: break
                
            AddClass(conn, SubjectName, YearLvl, True)
            # Create a new class and add into the joining table
            c.execute('''SELECT last_insert_rowid()''')
            classID = c.fetchone()
            c.execute('''INSERT INTO Teachers_Classes VALUES (?,?);''', (int(teacherID[0]), int(classID[0]))) 

        else:
            print(teacherID[0], available[0][0])
            c.execute('''INSERT INTO Teachers_Classes VALUES (?,?);''', (int(teacherID[0]), int(available[0][0])))    
        #If exists create a new class.
        SubjectName = None
        YearLvl = None
    print('Addition of Teacher successful')
    conn.commit()

def AddStudent(conn):
    c = conn.cursor()
    StudentName = SanitiseData(input('What is the students full name?: ')).split()
    if len(StudentName) != 2:
        print(f'{StudentName} can\'t automatically be split into first and last name')
        StudentFirstName = SanitiseData(input('Please enter the first name/names: '))
        StudentLastName = SanitiseData(input('Please enter the last name/names: '))
        StudentName = [StudentFirstName, StudentLastName]

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
                 WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl])
        classes = c.fetchall()
        
        if len(classes) == 0: # If Class doesn't exist

            print('You will need to create this class and add the teacher who teachers it') #TODO add existing teacher instead of creating new one?
            AddClass(conn, SubjectName, YearLvl, False)
            # Create a new class and add into the joining table
            c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl])
            classID = c.fetchone()
            c.execute('''INSERT INTO Students_Classes VALUES (?,?);''', (int(StudentID[0]), int(classID[0]))) 

        else:
            c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl])
            ClassIDs = c.fetchall()
            studentNumbers = []
            for Class in ClassIDs:
                c.execute(''' SELECT StudentsID from Students_Classes WHERE ClassesID = ?''', Class) #Returns the student's ID who take a class
                studentNumbers.append((Class, len(c.fetchall())))

            studentNumbers = sorted(studentNumbers, key=lambda x: x[1]) # Sorts the list of class numbers ascending
            c.execute('''INSERT INTO Students_Classes VALUES (?,?);''', [int(StudentID[0]), int(studentNumbers[0][0][0])]) # Adds the student to the lowest class
    
    print('Addition of Student successful')
    conn.commit()
