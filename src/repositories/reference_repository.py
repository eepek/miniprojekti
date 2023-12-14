"""Module for saving references"""
from entities.reference import Reference, ReferenceType
from constants import KEY_DOES_NOT_EXIST_ERROR, INVALID_REFERENCE_TYPE_ERROR
from database_connection import get_database_connection


class ReferenceRepository:
    """Class that interacts with database.
    """

    def __init__(self):
        """Class constructor, initializes database connection"""
        self._connection = get_database_connection()

    def save_to_file(self, file_path):
        """Save database to file in BibTeX form."""
        with open(file_path, "w", encoding="utf-8") as references_data:
            for reference in self.load_all():
                references_data.write(str(reference))
                references_data.write("\n")

    def save(self, reference):
        """Saves reference into database
        which can be read when displaying references
        to user

        Args:
            reference (Reference): Reference to be saved
        """

        cursor = self._connection.cursor()

        sql = """INSERT INTO Authors (author) VALUES (:author) ON CONFLICT DO NOTHING"""
        cursor.execute(sql, {"author": reference.fields["author"]})
        self._connection.commit()

        if "institution" in reference.fields:
            sql = """INSERT INTO Institutions (institution)
                VALUES (:institution) ON CONFLICT DO NOTHING"""
            cursor.execute(
                sql, {"institution": reference.fields["institution"]})
            self._connection.commit()

        if "booktitle" in reference.fields:
            sql = """INSERT INTO Booktitles (booktitle)
                VALUES (:booktitle) ON CONFLICT DO NOTHING"""
            cursor.execute(sql, {"booktitle": reference.fields["booktitle"]})
            self._connection.commit()

        if "editor" in reference.fields:
            sql = """INSERT INTO Editors (editor)
                VALUES (:editor) ON CONFLICT DO NOTHING"""
            cursor.execute(sql, {"editor": reference.fields["editor"]})
            self._connection.commit()

        if "series" in reference.fields:
            sql = """INSERT INTO Series (series)
                VALUES (:series) ON CONFLICT DO NOTHING"""
            cursor.execute(sql, {"series": reference.fields["series"]})
            self._connection.commit()

        if "type" in reference.fields:
            sql = """INSERT INTO Types (type) VALUES (:type) ON CONFLICT DO NOTHING"""
            cursor.execute(sql, {"type": reference.fields["type"]})
            self._connection.commit()

        sql = """INSERT INTO Referencetypes (referencetype)
                VALUES (:referencetype) ON CONFLICT DO NOTHING"""
        cursor.execute(sql, {"referencetype": str(reference.reference_type)})
        self._connection.commit()

        sql = """INSERT INTO Bibrefs (
                    key, title, author_id, year, institution_id, booktitle_id, editor_id,
                    referencetype_id, volume, type_id, number, series_id, pages, address,
                    month, note, annote, school, journal
              ) VALUES (?, ?, (SELECT id FROM Authors WHERE author = ?), ?,
              (SELECT id FROM Institutions WHERE institution = ?),
              (SELECT id FROM Booktitles WHERE booktitle = ?),
              (SELECT id FROM Editors WHERE editor = ?),
              (SELECT id FROM Referencetypes WHERE referencetype = ?), ?,
              (SELECT id FROM Types WHERE type = ?), ?,
              (SELECT id FROM Series WHERE series = ?), ?, ?, ?, ?, ?, ?, ?)
            """
        values = (
            reference.key, reference.fields["title"],
            reference.fields["author"], reference.fields["year"],
            None if "institution" not in reference.fields else reference.fields["institution"],
            None if "booktitle" not in reference.fields else reference.fields["booktitle"],
            None if "editor" not in reference.fields else reference.fields["editor"],
            str(reference.reference_type),
            None if "volume" not in reference.fields else reference.fields["volume"],
            None if "type" not in reference.fields else reference.fields["type"],
            None if "number" not in reference.fields else reference.fields["number"],
            None if "series" not in reference.fields else reference.fields["series"],
            None if "pages" not in reference.fields else reference.fields["pages"],
            None if "address" not in reference.fields else reference.fields["address"],
            None if "month" not in reference.fields else reference.fields["month"],
            None if "note" not in reference.fields else reference.fields["note"],
            None if "annote" not in reference.fields else reference.fields["annote"],
            None if "school" not in reference.fields else reference.fields["school"],
            None if "journal" not in reference.fields else reference.fields["journal"]
        )

        cursor.execute(sql, values)
        self._connection.commit()

    def load_all(self):
        """Loads all references from database

        Returns all references from database
        """

        cursor = self._connection.cursor()

        sql = """select Bibrefs.key from Bibrefs"""
        cursor.execute(sql)
        row = cursor.fetchall()
        if not row:
            return []
        references = []
        for r in row:
            references.append(self.load_one(r[0]))

        return references

    def load_one(self, search_key):
        """Retrieves reference by key

        Args:
            search_key (String): Key to determine correct reference
        Raises:
            ValueError: Raises, if key not found
        Returns:
            Reference: Reference or subclass object
        """
        cursor = self._connection.cursor()

        sql = """
                SELECT Referencetypes.referencetype, Bibrefs.key, Bibrefs.title, Authors.author, Bibrefs.year,
                    Institutions.institution, Booktitles.booktitle, Editors.editor, Bibrefs.volume, 
                    Types.type, Bibrefs.number, Series.series, Bibrefs.pages, Bibrefs.address,
                    Bibrefs.month, Bibrefs.note, Bibrefs.annote, Bibrefs.school, Bibrefs.journal
                FROM Bibrefs
                LEFT JOIN Authors ON Bibrefs.author_id = Authors.id
                LEFT JOIN Institutions ON Bibrefs.institution_id = Institutions.id
                LEFT JOIN Booktitles ON Bibrefs.booktitle_id = Booktitles.id
                LEFT JOIN Editors ON Bibrefs.editor_id = Editors.id
                LEFT JOIN Types ON Bibrefs.type_id = Types.id
                LEFT JOIN Series ON Bibrefs.series_id = Series.id
                LEFT JOIN Referencetypes ON Bibrefs.referencetype_id = Referencetypes.id
                WHERE Bibrefs.key = ?
            """
        key = (search_key, )
        cursor.execute(sql, key)

        row = cursor.fetchone()
        if not row:
            raise ValueError(KEY_DOES_NOT_EXIST_ERROR)

        if row[0] == "ReferenceType.TECHREPORT":
            reference_fields = {
                "title": row["title"],
                "author": row["author"],
                "institution": row["institution"],
                "year": row["year"],
                "type": row["type"],
                "number": row["number"],
                "address": row["address"],
                "month": row["month"],
                "note": row["note"],
                "annote": row["annote"]
            }
            return Reference(ReferenceType.TECHREPORT, row[1], reference_fields)

        if row[0] == "ReferenceType.INPROCEEDINGS":
            reference_fields = {
                "title": row["title"],
                "author": row["author"],
                "booktitle": row["booktitle"],
                "year": row["year"],
                "editor": row["editor"],
                "volume": row["volume"],
                "series": row["series"],
                "pages": row["pages"],
                "address": row["address"],
                "month": row["month"],
                "note": row["note"]
            }
            return Reference(ReferenceType.INPROCEEDINGS, row[1], reference_fields)

        if row[0] == "ReferenceType.ARTICLE":
            reference_fields = {
                "title": row["title"],
                "author": row["author"],
                "journal": row["journal"],
                "year": row["year"],
                "volume": row["volume"],
                "number": row["number"],
                "pages": row["pages"],
                "month": row["month"],
                "note": row["note"]
            }
            return Reference(ReferenceType.ARTICLE, row[1], reference_fields)

        if row[0] == "ReferenceType.PHD":
            reference_fields = {
                "title": row["title"],
                "author": row["author"],
                "school": row["school"],
                "year": row["year"],
                "type": row["type"],
                "address": row["address"],
                "month": row["month"],
                "note": row["note"]
            }
            return Reference(ReferenceType.PHD, row[1], reference_fields)

        raise ValueError(INVALID_REFERENCE_TYPE_ERROR)

    def delete_from_db(self, search_key):
        """Deletes reference from database by key"""

        cursor = self._connection.cursor()

        sql = "DELETE FROM Bibrefs WHERE key = ?"
        key = (search_key, )
        cursor.execute(sql, key)

        self._connection.commit()

    def get_similar_key_count(self, key: str) -> int:
        """Returns key substring occurrences in self._references
        Args:
            key (str): Key to be searched
        Returns:
            int: Amount of similar keys
        """
        return sum(key in reference.key for reference in self.load_all())

    def empty_all_tables(self):
        """Deletes all rows from all database tables
        """

        cursor = self._connection.cursor()
        tables = ["Bibrefs", "Authors", "Institutions", "Booktitles",
                  "Editors", "Series", "Types", "Referencetypes"]
        sql = "DELETE FROM"
        for table in tables:
            cursor.execute(f"{sql} {table}")

        self._connection.commit()
