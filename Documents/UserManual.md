# User Manual

## Purpose of the program

The program is to maintain a record of bibliographical references in BibTex format (.bib).

## Installation and configuration

1. Clone repository [Miniprojekti](https://github.com/eepek/miniprojekti)
2. install dependencies:

```bash
poetry install
```

## Starting the program

All command line actions to be run on project main folder.

1. Start Poetry shell:

```bash
poetry poetry shell
```

All following actions are to be run on Poetry shell.

2. Start Program:

```bash
python3 src/index.py
```

## Main view

Main view shows menu with following commands:

---

Welcome to your vault of references!

Command options:

1: Browse all references

2: Add reference (inproceedings)

c: Show command options

x: Exit

To view command options, type c

What would you like to do?:

---

Command is chosen by pressing key 1, 2, c or x from keyboard:

- 1: shows all references on screen
- 2: opens prompt to add new reference, see below for details
- c: shows main menu
- x: ends the program

### Add reference view

Choosing "Add reference (inproceedings)" opens prompt for inputting details of new reference. Prompt is asking one detail at the time. Mandatory fields must be inputted (they will be asked again), optional fields can be skipped by pressing enter. Below is list of asked details, with format requirements:

- Enter value for field key (mandatory): BibTex record identifier, free text
- Enter value for field title (mandatory): free text
- Enter value for field author (mandatory): free text
- Enter value for field booktitle (mandatory): free text
- Enter value for field year (mandatory): numerical in format YYYY
- Enter value for field editor (optional, enter to skip): free text
- Enter value for field volume (optional, enter to skip): numerical in format N (or NN or NNN, etc)
- Enter value for field series (optional, enter to skip): free text
- Enter value for field pages (optional, enter to skip): text in format pp-pp or pp (for single page articles)
- Enter value for field address (optional, enter to skip): free text
- Enter value for field month (optional, enter to skip): one of below formats:
  - month number 1-12
  - English standard abbreviation (jan, feb, mar, ...)
  - English full month name (January, February, ...)
- Enter value for field note (optional, enter to skip): free text

Program will check that each field is in required format, and in case it is not, error message is shown. If all fields in the inputted reference are in acceptable format, the reference will be saved into a file.
