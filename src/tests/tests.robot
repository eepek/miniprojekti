*** Settings ***
Library  ../AppLibrary.py
Library  PexpectLibrary
Library  DatabaseLibrary

*** Variables ***
${DB_FILE}  "data/test-database.sqlite"


*** Test Cases ***
As A User I Want The App To Use Database File
    Spawn  python3 src/index_gui.py
    Expect  GUI
    Send  a
    Expect  TechReport
    Expect  Inproceedings
    Send  o
    Expect  title
    Send Line  test_title
    Send  \t
    Send Line  test_author
    Send  \t
    Send Line  MIT
    Send  \t
    Send Line  1989
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  h
    Expect  Show all BibTex references
    Send  l
    Expect  test_au89
    Terminate
    Connect To Database Using Custom Params  sqlite3  ${DB_FILE}
    Check If Exists In Database  SELECT * FROM Bibrefs WHERE key='test_au89';
    Disconnect From Database

As A User I Can Delete References By Key
    Spawn  python3 src/index_gui.py
    Send  a
    Send  o
    Expect  title
    Send Line  Technical Report
    Send  \t
    Send Line  Powers, Austin
    Send  \t
    Send Line  MIT
    Send  \t
    Send Line  1965
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  h
    Send  l
    Send Control  j
    Send  d
    Send  y
    Expect  Show all BibTex references
    Set Delay After Terminate  3
    Terminate
    Connect To Database Using Custom Params  sqlite3  ${DB_FILE}
    Check If Not Exists In Database  SELECT * FROM Bibrefs WHERE key='Powers65';
    Disconnect From Database

As A User I Want To Modify Added References
    Spawn  python3 src/index_gui.py
    Send  l
    #Tää rivi modataan kun enter saadaan toimimaan
    Send Control  j
    Expect  title
    Send  \t
    Expect Exact  A report of
    Send Control  j
    Send  \x7f[C
    Send  \x7f[C
    Send  \x7f[C
    Send  \x7f[C
    Send  \x7f[C
    Send Control  j
    Set Delay After Terminate  3
    Terminate
    # Connect To Database Using Custom Params  sqlite3  ${DB_FILE}
    # Check If Exists In Database  SELECT * FROM Bibrefs WHERE title='A report of';
    # Disconnect From Database


# As a user I want to filter references by reference type, year or author
#     Spawn  python3 src/index_gui.py
#     Send  l
#     Expect Exact  Filter
#     Terminate
