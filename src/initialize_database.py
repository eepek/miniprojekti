""" Module to initialize database """
from database_connection import get_database_connection


def create_tables(connection):
    """ Creating tables"""

    # if not connection:
    #     print("error")

    cursor = connection.cursor()

    sql = """
        CREATE TABLE Authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT
        );
        """
    cursor.execute(sql)

    sql = """
    CREATE TABLE Institutions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        institution TEXT
    );
    """

    cursor.execute(sql)

    sql = """
    CREATE TABLE Booktitles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booktitle TEXT
    );
    """
    cursor.execute(sql)

    sql = """
        CREATE TABLE Editors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            editor TEXT
        );
        """
    cursor.execute(sql)

    sql = """
    CREATE TABLE Series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        series TEXT 
    );
    """
    cursor.execute(sql)

    sql = """
    CREATE TABLE Types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT
    );
    """
    cursor.execute(sql)

    sql = """
    CREATE TABLE Referencetypes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referencetype TEXT
    );
    """
    cursor.execute(sql)

    sql = """
    CREATE TABLE Bibrefs (
        key TEXT PRIMARY KEY UNIQUE,
        title TEXT NOT NULL,
        author_id INT NOT NULL REFERENCES Authors,
        year INT NOT NULL,
        institution_id INT REFERENCES Institutions,
        booktitle_id INT REFERENCES Booktitles,
        editor_id INT REFERENCES Editors,
        referencetype_id INT REFERENCES Referencetypes,
        volume TEXT,
        type_id INT REFERENCES Types,
        number TEXT,
        series_id INT REFERENCES Series,
        pages TEXT,
        address TEXT,
        month TEXT,
        note TEXT,
        annote TEXT
    );
    """
    cursor.execute(sql)

    connection.commit()


def drop_tables(connection):
    """ Deleting all tables """
    # if not connection:
    #     print("error")

    cursor = connection.cursor()

    sql = """
    DROP TABLE IF EXISTS Bibrefs
    """
    cursor.execute(sql)

    sql = """
    DROP TABLE IF EXISTS Authors
    """
    cursor.execute(sql)

    sql = """
    DROP TABLE IF EXISTS Institutions
    """
    cursor.execute(sql)

    sql = """
    DROP TABLE IF EXISTS Booktitles
    """
    cursor.execute(sql)

    sql = """
    DROP TABLE IF EXISTS Editors
    """
    cursor.execute(sql)

    sql = """
    DROP TABLE IF EXISTS Series
    """
    cursor.execute(sql)

    sql = """
    DROP TABLE IF EXISTS Types
    """
    cursor.execute(sql)

    sql = """
    DROP TABLE IF EXISTS Referencetypes
    """
    cursor.execute(sql)

    connection.commit()


def initialize_database():
    """ Initializes database deleting and creating new tables"""
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
