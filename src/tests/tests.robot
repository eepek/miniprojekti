*** Settings ***
Library  ../AppLibrary.py

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
    Run Program
