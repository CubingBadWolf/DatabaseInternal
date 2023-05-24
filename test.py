import csv
import string
import sqlite3

def ReadCSVtoDB(file, db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    tableName = file[:-4] # Removes the .csv at the end
    with open(file, 'r') as f:
        data = []
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
        f.close()

        headers = data.pop(0) #Removes the headers at the top of the csv and returns it to the variable
        containsID = False
        
        columnTypes = {}
        for header in headers:
            column_type = None
            for row in data:
                if row[headers.index(header)].isnumeric():
                    if header.casefold() == 'ID'.casefold():
                        column_type = 'INTEGER PRIMARY KEY AUTOINCREMENT'
                        containsID = True
                    else:
                        #If conflicting types found then make it default to text
                        if column_type == None or column_type == 'INTEGER NOT NULL': 
                            column_type = 'INTEGER NOT NULL'
                        else:
                            column_type = 'TEXT NOT NULL'
                else:
                    try:
                        float(row[headers.index(header)])
                        #If conflicting types found then make it default to text
                        if column_type == None or column_type == 'Real NOT NULL': 
                            column_type = 'REAL NOT NULL'
                        else:
                            column_type = 'TEXT NOT NULL'

                    except ValueError:
                        column_type = 'TEXT NOT NULL'
                    break 
            columnTypes[header] = column_type

        CreateQuery = f'CREATE TABLE {tableName} ('
        if not containsID:
            CreateQuery += 'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
        CreateQuery += ', '.join([f'{header} {column_type}' for header, column_type in columnTypes.items()])
        CreateQuery += ');'

        c.execute(CreateQuery)
            
        insert_query = f'INSERT INTO {tableName} VALUES ('
        if not containsID:
                insert_query += 'NULL, '
        insert_query += ', '.join(["?"] * len(headers))
        insert_query += ');'
        c.executemany(insert_query, data)        

        conn.commit()


def CreateJoiningTable(File, Database, Table1, Table2):
    conn = sqlite3.connect(Database)
    c = conn.cursor()

    with open(File, 'r') as f:
        data = []
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
        f.close()

    data.pop(0) #Removes headers as they are assigned by table name later

    tableName = File[:-4] #Removes .csv file ending

    # Retrieve primary key column names for table1
    c.execute(f"PRAGMA table_info({Table1})")
    table1_columns = c.fetchall()
    Table1_PK = next((column[1] for column in table1_columns if column[5] == 1), None)

    # Retrieve primary key column names for table2
    c.execute(f"PRAGMA table_info({Table2})")
    table2_columns = c.fetchall()
    Table2_PK = next((column[1] for column in table2_columns if column[5] == 1), None)

    if Table1_PK is None or Table2_PK is None:
        print("Unable to determine primary key columns.")
        return

    # Create the joining table
    c.execute(f'''CREATE TABLE {tableName} (
                        {Table1}ID INTEGER,
                        {Table2}ID INTEGER,
                        FOREIGN KEY ({Table1}ID) REFERENCES {Table1}({Table1_PK}),
                        FOREIGN KEY ({Table2}ID) REFERENCES {Table2}({Table2_PK})
                    )''')

    c.executemany(f'''INSERT INTO {tableName} Values (?,?)''', data)

    conn.commit()
    conn.close()


ReadCSVtoDB('Students.csv','test.db')
ReadCSVtoDB('Classes.csv','test.db')
ReadCSVtoDB('Teachers.csv','test.db')
CreateJoiningTable('Students_Classes.csv', 'test.db', 'Students', 'Classes')
CreateJoiningTable('Teachers_Classes.csv', 'test.db', 'Teachers', 'Classes')