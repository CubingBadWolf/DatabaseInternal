import os
from CreateDatabase import MakeDB
import tabulate
from SanitiseStrings import SanitiseData
from AddQueries import *
from SearchQueries import *
from UpdateQueries import *
from DeleteQueries import *

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

# Error prevention isn't the best TODO make it better. + TODO Check injection vulnerability

def menu():
    options = {
        "add": {
            "students": lambda: AddStudent(conn),
            "classes": lambda: AddClass(conn, None, None, False),
            "teachers": lambda: AddTeacher(conn, None, None)
        },
        "update": {
            "students": lambda: UpdateStudentINFO(conn, None),
            "teachers": lambda: UpdateTeacherINFO(conn, None)
        },
        "delete": {
            "students": lambda: DeleteStudent(conn, None),
            "classes": lambda: DeleteClass(conn, None),
            "teachers": lambda: DeleteTeacher(conn, None)
        },
        "view": {
            "students": {
                "classes": lambda: print(tabulate.tabulate(StudentsFromClass(None), headers=['First Name', 'Last Name', 'Year Level'], tablefmt='github') + '\n'),
                "teachers": lambda: print(tabulate.tabulate(StudentsFromTeachers(None), headers=['First Name', 'Last Name', 'Year Level'], tablefmt='github') + '\n'),
                "": lambda: print(tabulate.tabulate(AllStudents(), headers=['First Name', 'Last Name', 'Year Level'], tablefmt='github') + '\n')
            },
            "classes": {
                "students": lambda: print(tabulate.tabulate(ClassFromStudent(None), headers=['Class Name', 'Year Level'], tablefmt='github')),
                "teachers": lambda: print(tabulate.tabulate(ClassFromTeacher(None), headers=['Class Name', 'Year Level'], tablefmt='github')),
                "": lambda: print(tabulate.tabulate(AllClasses(), headers=['Class Name', 'Year Level'], tablefmt='github'))
            },
            "teachers": {
                "students": lambda: print(tabulate.tabulate(TeachersFromStudent(None), headers=['First Name', 'Last Name'], tablefmt='github')),
                "classes": lambda: print(tabulate.tabulate(TeacherFromClass(None), headers=['First Name', 'Last Name'], tablefmt='github')),
                "": lambda: print(tabulate.tabulate(AllTeachers(), headers=['First Name', 'Last Name'], tablefmt='github'))
            }
        }
    }

    option = input("Select an option [add, update, delete, view]: ")
    if option in options:
        sub_option = input(f"Select an option {list(options[option].keys())}: ").lower()
        if sub_option in options[option]:
            sub_sub_options = options[option][sub_option]
            if isinstance(sub_sub_options, dict):
                sub_sub_option = input(f"Select an option {list(sub_sub_options.keys())}: ").lower()
                try:
                    sub_sub_options[sub_sub_option]()
                    return True
                except KeyError:
                    print("Invalid option selected.")
                    return False

                except Exception as e:
                    print("An error occurred:", str(e))
                    return False

            else:
                try:
                    sub_sub_options()
                    return True
                except Exception as e:
                    print("An error occurred:", str(e))
                    return False
        else:
            print("Invalid option selected.")
            return False

    else:
        print("Invalid option selected.")
        return False


if __name__ == '__main__':
    if not os.path.exists('Database.db'):
        MakeDB()                

    end = False
    while not end:
        end = menu()

conn.close()