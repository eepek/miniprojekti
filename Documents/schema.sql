CREATE TABLE References (
    key TEXT PRIMARY KEY UNIQUE,
    title TEXT NOT NULL,
    author_id INT NOT NULL REFERENCES Authors,
    year INT NOT NULL,
    institution_id INT REFERENCES Institutions
    booktitle_id INT REFERENCES Booktitles,
    editor_id INT REFERENCES Editors,
    referecentype_id INT REFERENCES Referencetypes
    volume TEXT,
    type_id INT REFERENCES Types,
    number TEXT,
    series_id INT REFERENCES Series,
    pages TEXT,
    address TEXT,
    month TEXT,
    note TEXT
);    

CREATE TABLE Authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL
);

CREATE TABLE Institutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instituion TEXT NOT NULL
);

CREATE TABLE Booktitles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booktitle TEXT NOT NULL
);

CREATE TABLE Editors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    editor TEXT NOT NULL
);


CREATE TABLE Series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series TEXT NOT NULL
);


CREATE TABLE Types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);


CREATE TABLE Referencetypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referencetype TEXT NOT NULL
);

