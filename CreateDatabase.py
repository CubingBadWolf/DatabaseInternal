import sqlite3
from ReadCSV import ReadCSV

def BuildDB():

    Classes = ReadCSV('Classes.csv')
    Students = ReadCSV('Students.csv')
    Teachers = ReadCSV('Teachers.csv')
    Students_Classes = ReadCSV('Students_Classes.csv')
    Teachers_Classes = ReadCSV('Teachers_Classes.csv')
    # Generate 2D lists from csv files


    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    # Initilise connection to Database

    # something to prevent duplicating tables if already existing

    # Querys to create tables

    # Querys to insert data into tables

    conn.commit()