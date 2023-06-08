import sqlite3
import tabulate
from SanitiseStrings import SanitiseData
from AddQueries import AddClass
from SearchQueries import ClassFromStudent, ClassFromTeacher


def UpdateStudentINFO(conn, StudentID):
    if StudentID == None:
        while True:
            try: 
                StudentID = int(input("Enter the student's ID: "))
                break
            except:
                print('Please enter a valid number')

    c = conn.cursor()
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
    if updateCollumns != 0:
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
    
    c.execute(f'''SELECT first_name, last_name FROM Students WHERE ID = '{StudentID}'; ''')
    studentName = c.fetchall()
    print('Here are the classes they take:')
    studentClasses = ClassFromStudent(studentName[0])
    print(tabulate.tabulate(studentClasses, headers=['Class Name'], tablefmt='github'))
    while True:
        yn = input('Would you like to update any of these classes? y/n: ')
        if yn.lower() == 'y':
            while True:
                updateClass = input('How many do you want to update?: ')
                try:
                    updateClass = int(updateClass)
                    if updateClass < 0 or updateClass > len(studentClasses):
                        print('Please enter a valid amount of classes to update?:')
                    else:
                        for n in range(updateClass):
                            IDClass_Query = f'''SELECT Classes.ID, Classes.Name
                                                FROM Students
                                                JOIN Students_Classes ON Students.ID = Students_Classes.StudentsID
                                                JOIN Classes ON Students_Classes.ClassesID = Classes.ID
                                                WHERE Students.ID = '{StudentID}';'''
                            c.execute(IDClass_Query)
                            results = c.fetchall()
                            IDs = [Class[0] for Class in results]
                            print(tabulate.tabulate(results, headers=['ID','Class Name'], tablefmt='github'))
                            while True:
                                id = input('What is the ID of the class you would like to change: ')
                                try:
                                    id = int(id)
                                    if id not in IDs:
                                        print('Please enter a valid class ID')
                                    else:
                                        c.execute(f'''SELECT Year_Level FROM Students WHERE ID = '{StudentID}';''')
                                        YearLvl = c.fetchone()

                                        SubjectName = SanitiseData(input('Enter what subject you wish to update it to?: ')) 
                                        c.execute('''SELECT ID FROM Classes
                                                WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl[0]])
                                        classes = c.fetchall()

                                        if len(classes) == 0: # If Class doesn't exist
                                            print('You will need to create this class and add the teacher who teachers it')
                                            AddClass(conn, SubjectName, YearLvl[0], False)
                                        
                                            # Create a new class and add into the joining table
                                            c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?''',(SubjectName, YearLvl[0]))
                                            classID = c.fetchone()
                                            c.execute('''UPDATE Students_Classes Set ClassesID = ? WHERE ClassesID = ? AND StudentsID = ?;''', (int(classID[0]), int(id), int(StudentID))) 

                                        else:
                                            c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl[0]])
                                            ClassIDs = c.fetchall()
                                            studentNumbers = []
                                            for Class in ClassIDs:
                                                c.execute(''' SELECT StudentsID from Students_Classes WHERE ClassesID = ?''', Class) #Returns the student's ID who take a class
                                                studentNumbers.append((Class, len(c.fetchall())))

                                            studentNumbers = sorted(studentNumbers, key=lambda x: x[0]) # Sorts the list of class numbers ascending
                                            c.execute('''UPDATE Students_Classes SET ClassesID = ? WHERE ClassesID = ? AND StudentsID = ? ;''', [int(studentNumbers[0][0][0]), id, StudentID]) # Adds the student to the lowest class
                                        break
                                except ValueError:
                                    print('Please enter a number')
                        break
                except ValueError:
                    print('Please enter a number')
            conn.commit()
            break
        elif yn.lower() == 'n':
            break
        else:
            print('Please enter y or n')
    while True:
        conn.commit()
        print('Here are the classes they take:')
        studentClasses = ClassFromStudent(studentName[0])
        print(tabulate.tabulate(studentClasses, headers=['Class Name'], tablefmt='github'))

        YN = input('Would you like to add another class? y/n: ')
        if YN.lower() == 'n':
            break
        elif YN.lower() == 'y':
            newClass = SanitiseData(input('What is the name of the class that you are adding?: '))
            while True:
                YearLevel = input('What year level is this class?: ')
                if YearLevel != '9' and YearLevel != '10':
                    print('Please enter either 9 or 10')
                else: break
            classToAdd = (newClass,YearLevel)

            c.execute(f'''SELECT Classes.Name, Classes.Year_Level
            FROM Students
            JOIN Students_Classes ON Students.ID = Students_Classes.StudentsID
            JOIN Classes ON Students_Classes.ClassesID = Classes.ID
            WHERE Students.ID = {StudentID};''')
            listOfClasses = c.fetchall()
            if classToAdd in listOfClasses:
                print('This student already takes this class')
                continue
            else:
                c.execute('''SELECT Name, Year_Level FROM Classes;''')
                allClasses = c.fetchall()

                if classToAdd in allClasses:
                    c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', classToAdd)
                    ClassIDs = c.fetchall()
                    studentNumbers = []
                    for Class in ClassIDs:
                        c.execute(''' SELECT StudentsID from Students_Classes WHERE ClassesID = ?''', Class) #Returns the student's ID who take a class
                        studentNumbers.append((Class, len(c.fetchall())))

                    studentNumbers = sorted(studentNumbers, key=lambda x: x[1]) # Sorts the list of class numbers ascending
                    c.execute('''INSERT INTO Students_Classes VALUES (?,?);''', [StudentID, int(studentNumbers[0][0][0])])
                    continue
                else:
                    print('You will need to create this class and add the teacher who teachers it')
                    AddClass(conn, classToAdd[0], classToAdd[1], False)
                    # Create a new class and add into the joining table
                    c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', classToAdd)
                    classID = c.fetchone()
                    print(classID)
                    c.execute('''INSERT INTO Students_Classes VALUES (?,?);''', (StudentID, int(classID[0]))) 
                    continue

        else:
            print('Please enter y or n')
    print('Update successful')
    conn.commit()



def UpdateTeacherINFO(conn, TeacherID):
    if TeacherID == None:
        while True:
            try: 
                TeacherID = int(input("Enter the teacher's ID: "))
                break
            except:
                print('Please enter a valid number')

    c = conn.cursor()
    c.execute('''SELECT * FROM Teachers WHERE ID = ?;''', [TeacherID])
    info = c.fetchone()
    teacherInfo=[item for item in info]
    teacherInfo.pop(0) #Removes ID as that is not needed to update

    print('Here is the original entry')
    cursor = c.execute(f"SELECT * FROM Teachers;")
    collumns = [description[0] for description in cursor.description]
    collumns.pop(0) # Removes the ID collumn as that will never be changed

    print(tabulate.tabulate([teacherInfo], headers=collumns, tablefmt='github'))
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

    if updateCollumns != 0:
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
        c.execute(f'''UPDATE Teachers SET {collumns[collumn]} = ?
                    WHERE ID = {TeacherID}''',[changed])
    
    c.execute(f'''SELECT first_name, last_name FROM Teachers WHERE ID = '{TeacherID}'; ''')
    teacherName = c.fetchall()

    while True:
        conn.commit()
        print('Here are the classes they teach:')
        teacherClasses = ClassFromTeacher(teacherName[0])
        print(tabulate.tabulate(teacherClasses, headers=['Class Name', 'Year Level'], tablefmt='github'))

        yn = input('Would you like to update any of these classes? y/n: ')
        if yn.lower() == 'y':
            while True:
                updateClass = input('How many do you want to update?: ')
                try:
                    updateClass = int(updateClass)
                    if updateClass < 0 or updateClass > len(teacherClasses):
                        print('Please enter a valid amount of classes to update?:')
                    else:
                        for n in range(updateClass):
                            conn.commit()
                            IDClass_Query = f'''SELECT Classes.ID, Classes.Name, Classes.Year_Level
                                                FROM Teachers
                                                JOIN Teachers_Classes ON Teachers.ID = Teachers_Classes.TeachersID
                                                JOIN Classes ON Teachers_Classes.ClassesID = Classes.ID
                                                WHERE Teachers.ID = '{TeacherID}';'''
                            c.execute(IDClass_Query)
                            results = c.fetchall()
                            IDs = [Class[0] for Class in results]
                            print(tabulate.tabulate(results, headers=['ID','Class Name', 'Year Level'], tablefmt='github'))
                            while True:
                                id = input('What is the ID of the class you would like to change: ')
                                try:
                                    id = int(id)
                                    if id not in IDs:
                                        print('Please enter a valid class ID')
                                    else:
                                        SubjectName = SanitiseData(input('Enter what subject you wish to update it to?: ')) 

                                        while True:
                                            YearLvl = SanitiseData(input('Enter what year level this class would be for: '))
                                            if YearLvl != '9' and YearLvl != '10':
                                                print('Please enter 9 or 10')
                                            else:
                                                YearLvl = int(YearLvl)
                                                break

                                        c.execute('''SELECT ID FROM Classes
                                                WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl])
                                        classes = c.fetchall()

                                        if len(classes) == 0: # If Class doesn't exist
                                            print('This class is being added to the database')
                                            AddClass(conn, SubjectName, YearLvl, True)
                                        
                                            # Create a new class and add into the joining table
                                            c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?''',(SubjectName, YearLvl))
                                            classID = c.fetchone()
                                            c.execute('''UPDATE Teachers_Classes Set ClassesID = ? WHERE ClassesID = ? AND TeachersID = ?;''', (int(classID[0]), id, TeacherID)) 

                                        else:
                                            c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLvl])
                                            ClassIDs = c.fetchall()
                                            c.execute('''SELECT ClassesID FROM Teachers_Classes;''')
                                            TaughtClasses = c.fetchall() # Selects the classes listed in teachers_classes i.e are being taugh.

                                            available = []
                                            for ID in ClassIDs:
                                                if ID not in TaughtClasses:
                                                    available.append(ID)

                                            if len(available) == 0:
                                                print('This class is being added to the database')
                                                AddClass(conn, SubjectName, YearLvl, True)
                                        
                                                # Create a new class and add into the joining table
                                                c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?''',(SubjectName, YearLvl))
                                                classID = c.fetchall()
                                                c.execute('''UPDATE Teachers_Classes Set ClassesID = ? WHERE ClassesID = ? AND TeachersID = ?;''', (int(classID[-1][0]), id, TeacherID)) #Select the last item in the list (the one just made)

                                            else:
                                                c.execute('''UPDATE Teachers_Classes Set ClassesID = ? WHERE ClassesID = ? AND TeachersID = ?;''', (available[0][0], id, TeacherID))
                                        break
                                except ValueError:
                                    print('Please enter a number')
                        break
                except ValueError:
                    print('Please enter a number')
            conn.commit()
            break
        elif yn.lower() == 'n':
            break
        else:
            print('Please enter y or n')
        conn.commit()
    while True:
        conn.commit()
        print('Here are the classes they teach:')
        teachingClasses = ClassFromTeacher(teacherName[0])
        print(tabulate.tabulate(teachingClasses, headers=['Class Name', 'Year Level'], tablefmt='github'))

        YN = input('Would you like to add another class? y/n: ')
        if YN.lower() == 'n':
            break
        elif YN.lower() == 'y':
            newClass = SanitiseData(input('What is the name of the class that you are adding?: '))
            while True:
                YearLevel = input('What year level is this class?: ')
                if YearLevel != '9' and YearLevel != '10':
                    print('Please enter either 9 or 10')
                else: break
            classToAdd = (newClass,int(YearLevel))
            listOfClasses = [item[1:] for item in teacherClasses]
            if classToAdd in listOfClasses:
                print('This teacher already teaches this class')
                continue
            else:
                c.execute('''SELECT Name, Year_Level FROM Classes;''')
                allClasses = c.fetchall()

                if classToAdd in allClasses:
                    c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', [SubjectName, YearLevel])
                    ClassIDs = c.fetchall()
                    c.execute('''SELECT ClassesID FROM Teachers_Classes;''')
                    TaughtClasses = c.fetchall() # Selects the classes listed in teachers_classes i.e are being taugh.

                    available = []
                    for ID in ClassIDs:
                        if ID not in TaughtClasses:
                            available.append(ID)

                    if len(available) == 0:
                        print('This class is being added to the database')
                        AddClass(conn, SubjectName, YearLevel, True)
                                        
                        # Create a new class and add into the joining table
                        c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?''',(SubjectName, YearLevel))
                        classID = c.fetchall()
                        c.execute('''UPDATE Teachers_Classes Set ClassesID = ? WHERE ClassesID = ? AND TeachersID = ?;''', (int(classID[-1]), id, TeacherID)) #Select the last item in the list (the one just made)

                    else:
                        c.execute('''UPDATE Teachers_Classes Set ClassesID = ? WHERE ClassesID = ? AND TeachersID = ?;''', (available[0], id, TeacherID))
                    continue
                else:
                    print('This class is being added to the database')
                    AddClass(conn, classToAdd[0], classToAdd[1], True)
                    # Create a new class and add into the joining table

                    c.execute('''SELECT ID FROM Classes WHERE Name = ? AND Year_Level = ?;''', classToAdd)
                    classID = c.fetchone()

                    c.execute('''INSERT INTO Teachers_Classes VALUES (?,?);''', (TeacherID, int(classID[0]))) 
                    continue

        else:
            print('Please enter y or n')

    print('Update successful')
    conn.commit()