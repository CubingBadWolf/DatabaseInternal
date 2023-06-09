import os
from CreateDatabase import MakeDB
import sqlite3
import tabulate
from SanitiseStrings import SanitiseData
from AddQueries import AddClass, AddStudent, AddTeacher
from SearchQueries import StudentsFromClass,StudentsFromTeachers,TeachersFromStudent,TeacherFromClass,ClassFromStudent,ClassFromTeacher,AllStudents,AllTeachers,AllClasses
from UpdateQueries import UpdateStudentINFO,UpdateTeacherINFO
from DeleteQueries import DeleteClass,DeleteStudent,DeleteTeacher


# Error prevention isn't the best TODO make it better. + TODO Check injection vulnerability

def menu(conn):
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
                "classes": lambda: print(tabulate.tabulate(StudentsFromClass(conn,None), headers=['Id','First Name', 'Last Name', 'Year Level'], tablefmt='github') + '\n'),
                "teachers": lambda: print(tabulate.tabulate(StudentsFromTeachers(conn,None), headers=['First Name', 'Last Name', 'Year Level'], tablefmt='github') + '\n'),
                "": lambda: print(tabulate.tabulate(AllStudents(conn), headers=['First Name', 'Last Name', 'Year Level'], tablefmt='github') + '\n')
            },
            "classes": {
                "students": lambda: print(tabulate.tabulate(ClassFromStudent(conn,None), headers=['Id','Class Name', 'Year Level'], tablefmt='github')),
                "teachers": lambda: print(tabulate.tabulate(ClassFromTeacher(conn,None), headers=['Id','Class Name', 'Year Level'], tablefmt='github')),
                "": lambda: print(tabulate.tabulate(AllClasses(conn), headers=['Id','Class Name', 'Year Level'], tablefmt='github'))
            },
            "teachers": {
                "students": lambda: print(tabulate.tabulate(TeachersFromStudent(conn,None), headers=['Id','First Name', 'Last Name'], tablefmt='github')),
                "classes": lambda: print(tabulate.tabulate(TeacherFromClass(conn,None), headers=['Id','First Name', 'Last Name'], tablefmt='github')),
                "": lambda: print(tabulate.tabulate(AllTeachers(conn), headers=['Id','First Name', 'Last Name'], tablefmt='github'))
            }
        }
    }

    option = input("Select an option to apply to the database from these options [add, update, delete, view]: ")
    if option in options:
        sub_option = input(f"Select what tables you want to use infomation for. Here are the options {list(options[option].keys())}: ").lower()
        if sub_option in options[option]:
            sub_sub_options = options[option][sub_option]
            if isinstance(sub_sub_options, dict):
                sub_sub_option = input(f"Select an option to use as an additional result (i.e classes if you want to view _ from a class, you can press enter to return all items) {list(sub_sub_options.keys())}: ").lower()
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

    conn = sqlite3.connect('Database.db')
    while True:
        yn = input('Do you want to make a query to the database y/n:')
        if yn.lower() == 'n':
            break
        elif yn.lower() == 'y':
            queried = False
            while not queried:
                queried = menu(conn)
        else:
            print('Please enter y or n')
conn.close()