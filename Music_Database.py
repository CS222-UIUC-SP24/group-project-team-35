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
def create_table(cursor, table_name, columns):
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ()")
        for pairs in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD {pairs[0]} {pairs[1]}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

#Can be used to create a new database as well
def connect(path):
    try:
        return sqlite3.connect(path)
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None


"""
The array will be similar to previous arrays where it will be a tuple
The tuple will contain all the information to be inputted into a new row of the Table of a database
Example:


"""
def insert_array_row(cursor, table_name, array):
    try:
        for rows in array:
            cursor.execute(f"INSERT INTO {table_name} VALUES {rows}")
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def insert_row(cursor, table_name, row_tuple):
    try:
        cursor.execute(f"INSERT INTO {table_name} VALUES {row_tuple}")
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_row(cursor, table_name, column_name, column_value):
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = '{column_value}'")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
#retrieve the entire table
def retrieve_data(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []



def add_column(cursor,table_name, column_name, column_type):
    cursor.execute(f"ALTER TABLE {table_name} ADD {column_name} {column_type}")

def delete_column(cursor,table_name, column_name, column_type):
    cursor.execute(f"ALTER TABLE {table_name} DROP {column_name}")


#New functions
def list_tables(cursor):
    """
    Lists all tables in the database.

    :param cursor: SQLite cursor object.
    :return: List of table names.
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [table[0] for table in cursor.fetchall()]


def update_row(cursor, table_name, column_name, new_value, identifier_column, identifier_value):
    """
    Updates a specific row's column with a new value based on an identifier.

    :param cursor: SQLite cursor object.
    :param table_name: Name of the table.
    :param column_name: Name of the column to update.
    :param new_value: New value for the column.
    :param identifier_column: Column name used to identify the row to update.
    :param identifier_value: Value of the identifier column to select the row.
    """
    cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {identifier_column} = ?", (new_value, identifier_value))
