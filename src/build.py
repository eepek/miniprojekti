""" Module to build new database file """
from initialize_database import initialize_database


def build():
    """ Calls initialize_database """
    initialize_database()

if __name__ == "__main__":
    build()
