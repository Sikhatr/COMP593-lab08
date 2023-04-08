"""
Description:
 Creates the people table in the Social Network database
 and populates it with 200 fake people.

Usage:
 python create_db.py
"""
import sqlite3
from faker import Faker
from datetime import datetime
import os
import inspect


def main():
    global db_path
    db_path = os.path.join(get_script_dir(), 'social_network.db')
    create_people_table()
    populate_people_table()


def create_people_table():
    """Creates the people table in the database"""

    # Opens a connection to an SQLite database. # Returns a Connection object that represent the database connection. # A new database file will be created if it doesn't already exist.
    con = sqlite3.connect(db_path)

    # Get a Cursor object that can be used to run SQL queries on the database.
    cur = con.cursor()

    # Define an SQL query that creates a table named 'people'.
    create_ppl_tbl_query = """
    CREATE TABLE IF NOT EXISTS people
        ( 
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            email TEXT NOT NULL, 
            address TEXT NOT NULL, 
            city TEXT NOT NULL, 
            province TEXT NOT NULL, 
            bio TEXT, 
            age INTEGER, 
            created_at DATETIME NOT NULL, 
            updated_at DATETIME NOT NULL 
        ); 
    """
    # Execute the SQL query to create the 'people' table.
    cur.execute(create_ppl_tbl_query)

    # Commit (save) pending transactions to the database.
    con.commit()

    # Close the database connection.
    con.close()


def populate_people_table():
    """Populates the people table with 200 fake people"""
    # Opens a connection to an SQLite database. # Returns a Connection object that represent the database connection. # A new database file will be created if it doesn't already exist.
    con = sqlite3.connect(db_path)

    # Get a Cursor object that can be used to run SQL queries on the database.
    cur = con.cursor()

    add_person_query = """ 
        INSERT INTO people 
        ( 
            name, 
            email, 
            address, 
            city, 
            province, 
            bio, 
            age, 
            created_at, 
            updated_at 
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?); 
    """

    # Create a faker object for English Canadian locale
    fake = Faker("en_CA")

    for _ in range(200):
        new_person = (fake.name(),
                      fake.email(),
                      fake.address(),
                      fake.city(),
                      fake.administrative_unit(),
                      fake.sentence(nb_words=6),
                      fake.random_int(min=1, max=100),
                      datetime.now(),
                      datetime.now())

        # Execute query to add new person to people table
        cur.execute(add_person_query, new_person)

    con.commit()
    con.close()


def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    script_path = os.path.abspath(
        inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)


if __name__ == '__main__':
    main()

    con = sqlite3.connect('social_network.db')
cur = con.cursor()
# SQL query that creates a table named 'relationships'.
create_relationships_tbl_query = """
 CREATE TABLE IF NOT EXISTS relationships
 (
 id INTEGER PRIMARY KEY,
 person1_id INTEGER NOT NULL,
 person2_id INTEGER NOT NULL,
 type TEXT NOT NULL,
 start_date DATE NOT NULL,
 FOREIGN KEY (person1_id) REFERENCES people (id),
 FOREIGN KEY (person2_id) REFERENCES people (id)
 );
"""
# Execute the SQL query to create the 'relationships' table.
cur.execute(create_relationships_tbl_query)
con.commit()
con.close()
