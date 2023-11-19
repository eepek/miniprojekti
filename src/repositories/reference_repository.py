"""Module for saving references"""
import bibtexparser
from entities.reference import Inproceedings
from constants import INPROCEEDINGS_KEYS, INPROCEEDINGS_MANDATORY_KEYS


class ReferenceRepository:
    """Class that interacts with database.
    Currently using .bib file in the folder /data/
    """

    def __init__(self, file_path):
        self._references = []
        self._file_path = file_path
        self.init_references()

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

            missing_mandatory_keys = set(INPROCEEDINGS_MANDATORY_KEYS) # copy
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

    def load_all(self):
        """Returns all the references currently in
        working memory on references list

        Returns:
            list: List of all references
        """
        return self._references

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
