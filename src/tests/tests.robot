*** Settings ***
Library  ../app_library.py

*** Test Cases ***
Adding Inproceedings Works
    Command  2
    Command  inproceedings
    Command  title_value
    Command  author_value
    Command  booktitle_value
    Command  2000
    Command  \
    Command  \
    Command  \
    Command  \
    Command  \
    Command  \
    Command  \
    Command  1
    Command  x
    Run Program
    Output Should Contain  {author_value}

Shutting Down Works
    Command  x
    Run Program
    Output Should Contain  Shutting down

Mandatory Field Is Required
    Command  2
    Command  inproceedings
    Command  \
    Run Program
    Output Should Contain  Field is mandatory
