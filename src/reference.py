"""Module consisting of parent class Reference and it's children."""
class Reference:
    """Parent class for all Bibtex- entry types
    """
    def __init__(self, key, title):
        self.key = key
        self.title = title

class Inproceedings(Reference):
    """Bibtex entry- type inproceeding

    Args:
        Reference (class): parent class, key & title
    """
    def __init__(self, key, title, author, booktitle, year,
                 editor = None, volume = None, series = None,
                 pages = None, address = None, month = None,
                 note = None):
        super().__init__(key, title)
        self.author = author
        self.booktitle = booktitle
        self.year = year
        self.editor = editor
        self.volume = volume
        self.series = series
        self.pages = pages
        self.address = address
        self.month = month
        self.note = note

    def __str__(self):
        """Constructs a dict of objects values and then
        goes thru the dict and creates bibtex fields if the
        value is not None.

        Returns:
            String: returns string in Bibtex- format
        """
        fields = {"author": self.author,
            "title": self.title,
            "booktitle": self.booktitle,
            "year": self.year,
            "editor": self.editor,
            "volume": self.volume,
            "series": self.series,
            "pages": self.pages,
            "address": self.address,
            "month": self.month,
            "note": self.note}

        bibtex_entries = []
        for key, value in fields.items():
            if value is not None:
                bibtex_entries.append(f"{key} = {{{value}}}")

        return f"@inproceedings{{{self.key},\n" + ",\n".join(bibtex_entries) + "\n}"
