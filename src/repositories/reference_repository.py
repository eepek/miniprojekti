"""Module for saving references"""
import bibtexparser
from entities.reference import Inproceedings
from constants import INPROCEEDINGS_KEYS, INPROCEEDINGS_MANDATORY_KEYS, KEY_DOES_NOT_EXIST_ERROR
# from database_connection import get_database_connection


class ReferenceRepository:
    """Class that interacts with database.
    Currently using .bib file in the folder /data/
    """

    def __init__(self, file_path):
        self._references = []
        self._file_path = file_path
        self.init_references()
        # self._connection = get_database_connection()  # temp should be init parameter

    def init_references(self):
        """Loads Inproceedings references from
        database file and saves them into _references
        list.
        """
        self._references = []
        with open(self._file_path, "r", encoding="utf-8") as references_data:

            bib_data = bibtexparser.load(references_data)

        for entry in bib_data.entries:
            ref_prototype = {
                "key": entry["ID"]
            }

            missing_mandatory_keys = set(INPROCEEDINGS_MANDATORY_KEYS)  # copy
            missing_mandatory_keys.remove("key")

            for key, value in entry.items():
                if key in INPROCEEDINGS_KEYS:
                    ref_prototype[key] = value
                    if key in INPROCEEDINGS_MANDATORY_KEYS:
                        missing_mandatory_keys.remove(key)

            # If haven't found all mandatory keys, don't load this entry
            if len(missing_mandatory_keys) > 0:
                continue

            new_reference = Inproceedings(**ref_prototype)
            self._references.append(new_reference)

    def save(self, reference: Inproceedings):
        """Saves reference into references list
        which can be read when displaying references
        to user

        Args:
            reference (Inproceedings): Reference to be saved
        """
        self._references.append(reference)
        with open(self._file_path, "a", encoding="utf-8") as references_data:
            references_data.write("\n")
            references_data.write(str(reference))

        # self.save_to_db(reference)

    # def save_to_db(self, reference: Inproceedings):
    #     """Saves reference into database

    #     Args:
    #         reference (Inproceedings): Reference to be saved
    #     """

    #     cursor = self._connection.cursor()

    #     sql = """INSERT INTO Authors (author) VALUES (:author) ON CONFLICT DO NOTHING"""
    #     cursor.execute(sql, {"author": reference.author})
    #     self._connection.commit()

    #     sql = """INSERT INTO Institutions (institution)
    #             VALUES (:institution) ON CONFLICT DO NOTHING"""
    #     cursor.execute(sql, {"institution": None})
    #     self._connection.commit()

    #     sql = """INSERT INTO Booktitles (booktitle) VALUES (:booktitle) ON CONFLICT DO NOTHING"""
    #     cursor.execute(sql, {"booktitle": reference.booktitle})
    #     self._connection.commit()

    #     sql = """INSERT INTO Editors (editor) VALUES (:editor) ON CONFLICT DO NOTHING"""
    #     cursor.execute(sql, {"editor": reference.editor})
    #     self._connection.commit()

    #     sql = """INSERT INTO Series (series) VALUES (:series) ON CONFLICT DO NOTHING"""
    #     cursor.execute(sql, {"series": reference.series})
    #     self._connection.commit()

    #     sql = """INSERT INTO Types (type) VALUES (:type) ON CONFLICT DO NOTHING"""
    #     cursor.execute(sql, {"type": None})
    #     self._connection.commit()

    #     sql = """INSERT INTO Referencetypes (referencetype)
    #             VALUES (:referencetype) ON CONFLICT DO NOTHING"""
    #     cursor.execute(sql, {"referencetype": None})
    #     self._connection.commit()

    #     sql = """INSERT INTO Bibrefs (
    #                 key, title, author_id, year, institution_id, booktitle_id, editor_id,
    #                 referecentype_id, volume, type_id, number, series_id, pages, address,
    #                 month, note
    #             ) VALUES (?, ?, (SELECT id FROM Authors WHERE author = ?), ?,
    #             (SELECT id FROM Institutions WHERE institution = ?), (SELECT id FROM Booktitles WHERE booktitle = ?),
    #             (SELECT id FROM Editors WHERE editor = ?), (SELECT id FROM Referencetypes WHERE referencetype = ?), ?,
    #             (SELECT id FROM Types WHERE type = ?), ?, (SELECT id FROM Series WHERE series = ?), ?, ?, ?, ?)
    #         """
    #     values = (
    #         reference.key, reference.title, reference.author, reference.year,
    #         "NULL", reference.booktitle, reference.editor,
    #         None, reference.volume, None,
    #         None, reference.series, reference.pages,
    #         reference.address, reference.month, reference.note
    #     )

    #     cursor.execute(sql, values)
    #     self._connection.commit()

    def load_all(self):
        """Returns all the references currently in
        working memory on references list

        Returns:
            list: List of all references
        """
        return self._references

    def load_one(self, search_key):
        """Retrieves reference by key

        Args:
            search_key (String): Key to determine correct reference
        Raises:
            ValueError: Raises, if key not found
        Returns:
            Reference: Reference or subclass object
        """
        reference = [ref for ref in self._references if ref.key == search_key]
        if reference:
            return reference[0]
        raise ValueError(KEY_DOES_NOT_EXIST_ERROR)

    def get_similar_key_count(self, key: str) -> int:
        """Returns key substring occurrences in self._references
        Args:
            key (str): Key to be searched
        Returns:
            int: Amount of similar keys
        """
        return sum(key in reference.key for reference in self._references)

    def file_lines(self):
        """Helper function for testing

        Returns:
            int: Number of lines in set use file
        """
        with open(self._file_path, "r", encoding="utf-8") as file:
            lines = len(file.readlines())

        return lines

    def empty_all_references(self):
        """Deletes all content in database .bib file
        """
        with open(self._file_path, "w", encoding="utf-8"):
            pass
