# User Manual

## Purpose of the program

The program is to maintain a record of bibliographical references in BibTex format (.bib).

## Installation and configuration

1. Clone repository [Miniprojekti](https://github.com/eepek/miniprojekti)
2. install dependencies:

```bash
poetry install
```

3. Build / initialize database

```bash
poetry run invoke build
```

Note! Build database empties all previously recorded data. Only to be run on first installation.

## Starting the program

All command line actions to be run on project main folder.

To start program run:

```bash
poetry run python3 src/index_gui.py
```

## Main view

Main view shows main menu with options:

![Home](manual_img/main_view.png)

You can interact with the GUI using mouse, or keyboard. On the main menu you can open a .bib file and load it to the database the program uses. If you don't have a .bib file, do not worry. You can create new references by adding them one by one and then export them to a .bib file that you can use with your LaTeX document.

## Show all view

When choosing to view all references, program opens a scrollable view of all the references. In this view you can search your vault of references with our filtering widget. Choose the value you wish to filter with and input your search parameter. Filtering reacts to each keystroke.

![All_refrences](manual_img/all_references.png)


### Add reference view

Choosing "Add reference" opens a view which shows you the available reference types:

![Select_type](manual_img/add_new_select_type.png)


Supported reference types:
inproceedings, techreport, article, phd.

After selecting the reference type you can input the relevant reference fields. After you have entered the input, you can proceed and save the reference or cancel. If you choose to save the reference, program checks for mandatory fields and and informs the user if there are any problems.

![Select_type](manual_img/insert_reference_info.png)


### View references by key view

Choosing "View reference by key" displays all the BibTex- reference keys in working memory.


![Show_keys](manual_img/listkeys.png)

From this view you can open a single reference. When you have opened the reference you can modify or delete the reference. To modify the field you must choose the field you wish to modify and then correct the value. The input is validated in the same way as it was when adding a new reference. 

![Single_reference](manual_img/single_reference.png)
