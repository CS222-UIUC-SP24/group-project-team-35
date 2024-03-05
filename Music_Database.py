import sqlite3


"""
For column_type there are 5 possible data types:
1) text
2) integer
3) real (real numbers that include decimals)
4) blob (anything in its raw form, this can include mp3 files, images, etc)
5) Null (An operator that tests for Null or empty values in column)
"""
def create_testing():
    pass

"""
columns is an array of tuples where the indicies each have a different meaning:
Index 1: The name of the column
Index 2: Data type of the column
"""
def create_table(cursor,table_name, columns):
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} ()
    """)

    for pairs in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD {pairs[0]} {pairs[1]}")


#Can be used to create a new database as well
def connect(path):
    return sqlite3.connect(path)


"""
The array will be similar to previous arrays where it will be a tuple
The tuple will contain all the information to be inputted into a new row of the Table of a database
Example:


"""
def insert_array_row(cursor, table_name, array):
    for rows in array:
        cursor.execute(f"INSERT INTO {table_name} VALUES {rows}")




def insert_row(cursor, table_name, tuple):
    cursor.execute(f"INSERT INTO {table_name} VALUES {tuple}")

def delete_row(cursor,table_name, column_name, column_value):
    cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = {column_value}")

#retrieve the entire table
def retrieve_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    
    return cursor.fetchall()



def add_column(cursor,table_name, column_name, column_type):
    cursor.execute(f"ALTER TABLE {table_name} ADD {column_name} {column_type}")

def delete_column(cursor,table_name, column_name, column_type):
    cursor.execute(f"ALTER TABLE {table_name} DROP {column_name}")
    

