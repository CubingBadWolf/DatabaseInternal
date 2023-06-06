import sqlite3


def DeleteClass(conn, ID):
    c = conn.cursor()
    c.execute("DELETE FROM Classes WHERE ID = ?", [ID])
    c.execute("DELETE FROM Students_Classes WHERE ClassesID = ?",[ID])
    c.execute("DELETE FROM Teachers_Classes WHERE ClassesID = ?",[ID])
    conn.commit()

def DeleteTeacher(conn, ID):
    c = conn.cursor()
    c.execute("DELETE FROM Teachers WHERE ID = ?", [ID])
    c.execute("DELETE FROM Teachers_Classes WHERE TeachersID = ?",[ID])
    conn.commit()

def DeleteStudent(conn, ID):
    c = conn.cursor()
    c.execute("DELETE FROM Students WHERE ID = ?", [ID])
    c.execute("DELETE FROM Students_Classes WHERE StudentsID = ?",[ID])
    conn.commit()