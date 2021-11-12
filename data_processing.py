import pandas as pd
import sqlite3
import os
import re

def get_shooting_data(path = "data.csv"):
    '''
    produces csv file "data.csv" with latest version of washington post database
    '''
    dirty = "dirty_data.csv"

    url = "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv"
    pd.read_csv(url, index_col = "id").to_csv(dirty)

    file = open(path, 'wt')
    # this is where all data cleaning takes place
    with open(dirty, 'rt') as f:
        for line in f:
            line = re.sub(' +', ' ', line) # removes extra spaces
            file.write(line)
    file.close()
    os.remove(dirty)


def edit_features(path = "data.csv"):
    '''
    function for all feature engineering prior to being loaded into a relational database
    '''
    data = pd.read_csv(path, index_col = "id")
    data[['year', 'month', 'day']] = data['date'].str.split('-', expand = True)
    data.to_csv(path)


def load_db(path = 'data.csv', database = "shooting.db"):
    '''
    loads data in csv file into a relational database for easy querying
    '''
    # because the dataset is so small it is significantly 
    # easier to create a new database each time the data is updated
    # then to only add the new rows
    if os.path.isfile(database):
        os.remove(database)

    conn = sqlite3.connect(database)
    curs = conn.cursor()
    sql = """CREATE TABLE tShooting (id INTEGER PRIMARY KEY,
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
    
    data = pd.read_csv(path)
    insert_row = "INSERT INTO tShooting VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    for row in data.values:
        curs.execute(insert_row, tuple(row))
        
    conn.commit()
    conn.close()


def view_schema(database = "shooting.db"):
    '''
    prints out database schema
    '''
    conn = sqlite3.connect(database)
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


def view_tShooting(database = "shooting.db"):
    '''
    prints first five rows of tShooting to help confirm everything was loaded correctly
    '''
    conn = sqlite3.connect(database)
    x = pd.read_sql(""" SELECT * 
                        FROM tShooting;""", conn)
    print(x.head())


def main():

    path = "data.csv"
    database = "shooting.db"

    get_shooting_data(path)
    edit_features(path)
    load_db(path, database)
    view_schema(database)
    view_tShooting(database)


if __name__ == "__main__":
    main()

    