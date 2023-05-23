import sqlite3
import os
from ReadCSV import ReadCSV

def BuildDB():

    # prevents duplicating tables if already existing
    if(os.path.exists('Database.db')):
        return 0

    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    # Initilise connection to Database

    c.execute('''CREATE TABLE Classes 
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Year_Level INTEGER NOT NULL);
        ''')
    
    c.execute('''CREATE TABLE Teachers 
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL);
        ''')
    
    c.execute('''CREATE TABLE Students 
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL, 
        Year_Level INTEGER NOT NULL);
        ''')

    c.execute('''CREATE TABLE Teachers_Classes 
        (TeacherID INTEGER, ClassID INTEGER,
        FOREIGN KEY (TeacherID) REFERENCES Teachers(ID),
        FOREIGN KEY (ClassID) REFERENCES Class(ID)
        );''')
    
    c.execute('''CREATE TABLE Students_Classes 
        (StudentID INTEGER, ClassID INTEGER,
        FOREIGN KEY (StudentID) REFERENCES Students(ID),
        FOREIGN KEY (ClassID) REFERENCES Class(ID)
        );''')
    # Querys to create tables

    #TODO Make function to automatically insert into tables from the csv. 
    Classes = ReadCSV('Classes.csv')
    Students = ReadCSV('Students.csv')
    Teachers = ReadCSV('Teachers.csv')
    Students_Classes = ReadCSV('Students_Classes.csv')
    Teachers_Classes = ReadCSV('Teachers_Classes.csv')
    Classes.pop(0)
    Students.pop(0)
    Teachers.pop(0)
    Students_Classes.pop(0)
    Teachers_Classes.pop(0)
    #Creates lists from csv, removes the first row which are the headers
    c.executemany('''INSERT INTO Classes(ID, Name, Year_Level) VALUES(?,?,?)''', Classes)
    c.executemany('''INSERT INTO Teachers(ID, First_Name, Last_Name) VALUES(?,?,?)''', Teachers)
    c.executemany('''INSERT INTO Students(ID, First_Name, Last_Name, Year_Level) VALUES(?,?,?,?)''', Students)
    c.executemany('''INSERT INTO Teachers_Classes(TeacherID, ClassID) VALUES(?,?)''', Teachers_Classes)
    c.executemany('''INSERT INTO Students_Classes(StudentID, ClassID) VALUES(?,?)''', Students_Classes)
    # Querys to insert data into tables

    conn.commit()