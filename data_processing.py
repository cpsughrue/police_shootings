import pandas as pd
import sqlite3
import os
import re

def get_data():
    '''
    produces csv file "data.csv" with latest version of washington post database
    '''
    dirty = "dirty_data.csv"
    clean = "data.csv"

    url = "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv"
    pd.read_csv(url, index_col="id").to_csv(dirty)

    file = open(clean, 'wt')
    with open("dirty_data.csv", 'rt') as f:
        for line in f:
            line = re.sub(' +', ' ', line)
            file.write(line)
    file.close()
    os.remove(dirty)

def edit_features():
    '''
    function for all feature engineering prior to being loaded into a relational database
    '''
    path = "data.csv"
    data = pd.read_csv(path, index_col="id")
    data[['year', 'month', 'day']] = data['date'].str.split('-', expand=True)
    data.to_csv(path)


def load_db():
    '''
    loads data in csv file into a relational database for easy querying
    '''
    data = pd.read_csv('data.csv')

    database = "shooting.db"
    if os.path.isfile(database):
        os.remove(database)

    conn = sqlite3.connect("shooting.db")
    curs = conn.cursor()

    sql = """CREATE TABLE tShooting (
            id INTEGER PRIMARY KEY,
            name TEXT,
            date TEXT,
            manner_of_death TEXT,
            armed TEXT,
            age INTEGER,
            gender TEXT,
            race TEXT,
            city TEXT,
            state TEXT,
            signs_of_mental_illness TEXT,
            threat_level TEXT,
            flee TEXT,
            body_camera TEXT,
            longitude REAL,
            latitude REAL,
            is_geocoding_exact TEXT,
            year INTEGER,
            month INTEGER,
            day INTEGER);"""

    curs.execute(sql)
    sql = "INSERT INTO tShooting VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    for row in data.values:
        curs.execute(sql, tuple(row))
    conn.commit()
    conn.close()

def view_schema():
    '''
    prints out database schema
    '''
    conn = sqlite3.connect("shooting.db")
    x = pd.read_sql(""" SELECT name 
                        FROM sqlite_master
                        WHERE type = 'table'
                        AND name LIKE 't%';""", conn)
    
    for table in x.values:
        sql = "PRAGMA table_info(" + table[0] + ");"
        print(table)
        print(pd.read_sql(sql, conn))
        print('\n')
        
    conn.close()