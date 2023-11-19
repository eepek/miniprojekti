from entities.reference import Inproceedings


class ReferenceRepository:
    """Class that interacts with database.
    Currently using .bib file in the folder /data/
    """

    def __init__(self, file_path):
        self._references = []
        self._file_path = file_path

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
        with open(self._file_path, "w", encoding="utf-8") as file:
            pass
