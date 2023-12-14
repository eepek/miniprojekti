*** Settings ***
Library  ../AppLibrary.py
Library  PexpectLibrary
Library  DatabaseLibrary
Suite Setup  Empty All Tables

*** Variables ***
${DB_FILE}  "data/test-database.sqlite"
${right_key}  '\x1b[C'
${down_key}  '\x1b[D'


*** Test Cases ***
As A User I Want The App To Use Database File
    #Tests also adding of techreport reference
    Spawn  python3 src/index_gui.py
    Expect  Vault of References
    Send  a
    Expect  techreport
    Expect  inproceedings
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
    Expect  Show all references
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
    Sleep  2s
    Expect  Show all references
    Send  l
    Expect  test_au89
    Send Control  j
    Close
    Connect To Database Using Custom Params  sqlite3  ${DB_FILE}
    Check If Not Exists In Database  SELECT * FROM Bibrefs WHERE key='powers65';
    Disconnect From Database

As A User I Want To Modify Added References
    Spawn  python3 src/index_gui.py
    Send  l
    #Tää rivi modataan kun enter saadaan toimimaan
    Send Control  j
    Expect  title
    Send  ${right_key}
    Send Control  j
    Send Line  ForRobotTestingPurposesOnly
    Send Control  j
    Send  s
    Expect  test_titleForRobotTestingPurposesOnly
    Set Delay After Terminate  3
    Terminate
    Connect To Database Using Custom Params  sqlite3  ${DB_FILE}
    Check If Exists In Database  SELECT * FROM Bibrefs WHERE title='test_titleForRobotTestingPurposesOnly';
    Disconnect From Database


As a user I want to filter references by reference type, year or author
    Spawn  python3 src/index_gui.py
    #Adding another entry to database
    Send  a
    Send  o
    Sleep  1s
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
    #Filtering results
    Send  s
    Sleep  2s
    Expect  Filter
    Send  1965
    Send  \t
    Send  ${right_key}
    Send  \n
    #Powers, Austin is found
    Expect  Powers, Austin
    #test_author is not found
    Expect  ${{['test_author', pexpect.EOF, pexpect.TIMEOUT]}}
    Close

As A User I Can Add Inproceedings Reference to App
    Spawn  python3 src/index_gui.py
    Expect  Vault of References
    Send  a
    Expect  techreport
    Expect  inproceedings
    Send  ${down_key}
    Send  o
    Expect  title
    Send Line  test_title
    Send  \t
    Send Line  test_author
    Send  \t
    Send Line  MIT
    Send  \t
    Send Line  1999
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  h
    Sleep  3s
    Expect  Show all references
    Send  l
    Expect  test_au99
    Terminate

As A User I Can Add Article Reference To App
    Spawn  python3 src/index_gui.py
    Expect  Vault of References
    Send  a
    Expect  techreport
    Expect  inproceedings
    Expect  article
    Send  ${down_key}
    Send  ${down_key}
    Send  o
    Expect  title
    Send Line  test_title
    Send  \t
    Send Line  test_author
    Send  \t
    Send Line  MIT
    Send  \t
    Send Line  2000
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  h
    Expect  Show all references
    Send  l
    Expect  test_au00
    Terminate

As A User I Can Add Phd Reference To App
    Spawn  python3 src/index_gui.py
    Expect  Vault of References
    Send  a
    Expect  techreport
    Expect  inproceedings
    Expect  article
    Send  ${down_key}
    Send  ${down_key}
    Send  ${down_key}
    Send  o
    Expect  title
    Send Line  test_title
    Send  \t
    Send Line  test_author
    Send  \t
    Send Line  MIT
    Send  \t
    Send Line  2010
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  \t
    Send  h
    Sleep  2s
    Expect  Show all references
    Send  l
    Expect  test_au10
    Terminate

As A User I Can List References by Key Value
    Spawn  python3 src/index_gui.py
    Expect  Vault of References
    Send  l
    Sleep  3s    Waiting for list to load
    Expect  test_au89
    Expect  test_au99
    Expect  test_au00
    Expect  test_au10
    Close