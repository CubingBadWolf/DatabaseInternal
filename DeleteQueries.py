import sqlite3


def DeleteClass(conn, ID):
    if ID == None:
        while True:
            try: 
                ID = int(input("Enter the class's ID: "))
                break
            except:
                print('Please enter a valid number')

    c = conn.cursor()
    c.execute("DELETE FROM Classes WHERE ID = ?", [ID])
    c.execute("DELETE FROM Students_Classes WHERE ClassesID = ?",[ID])
    c.execute("DELETE FROM Teachers_Classes WHERE ClassesID = ?",[ID])
    print('Deletion successful')
    conn.commit()

def DeleteTeacher(conn, ID):
    if ID == None:
        while True:
            try: 
                ID = int(input("Enter the Teacher's ID to delete: "))
                break
            except:
                print('Please enter a valid number')

    c = conn.cursor()
    c.execute("DELETE FROM Teachers WHERE ID = ?", [ID])
    c.execute("DELETE FROM Teachers_Classes WHERE TeachersID = ?",[ID])

    print('Deletion successful')
    conn.commit()

def DeleteStudent(conn, ID):
    if ID == None:
        while True:
            try: 
                ID = int(input("Enter the student's ID to delete: "))
                break
            except:
                print('Please enter a valid number')

    c = conn.cursor()
    c.execute("DELETE FROM Students WHERE ID = ?", [ID])
    c.execute("DELETE FROM Students_Classes WHERE StudentsID = ?",[ID])

    print('Deletion successful')
    conn.commit()