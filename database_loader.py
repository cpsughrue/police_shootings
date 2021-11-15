import sqlite3
import pandas as pd

def load_shooting_db(path = "./data/shooting.csv", database = "./data/shooting.db"):
    '''
    loads shooting.csv into a relational database
    '''
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    # because the dataset is so small it is significantly 
    # easier to recreate the table each time the data is
    # updated then to only add the new rows
    curs.execute("DROP TABLE IF EXISTS tShooting;")
    
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


def view_db_schema(database: str) -> None:
    '''
    prints out sqlite database schema
    '''
    conn = sqlite3.connect(database)
    # list of tables in the database
    tables: list[str] = pd.read_sql("""SELECT name 
                                       FROM sqlite_master
                                       WHERE type = 'table';""", conn).loc[:, "name"].values

    for table in tables:
        print(table)
        print(pd.read_sql(f"""PRAGMA table_info({table});""", conn))
        print('\n')

    conn.close()


def table_head(database: str, table: str) -> None:
    '''
    print first five rows of a table to help confirm everything was loaded correctly
    '''
    conn = sqlite3.connect(database)
    print(pd.read_sql(f"""SELECT * FROM {table} LIMIT 5;""", conn))
    conn.close()


def main():
    database = "./data/shooting.db"
    view_db_schema(database)
    table_head(database,  table = "tShooting")


if __name__ == "__main__":
    main()
    