""" Module to initialize database """
from database_connection import get_database_connection

def create_tables(connection):
    """ Creating tables"""
    if not connection:
        print("error")

def drop_tables(connection):
    """ Deleting all tables """
    if not connection:
        print("error")


def initialize_database():
    """ Initializes database deleting and creating new tables"""
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
