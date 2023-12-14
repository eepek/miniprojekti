"""Unittests for reference module"""
import unittest
import pytest
import os
from repositories.reference_repository import ReferenceRepository
from entities.reference import Reference
from constants import KEY_DOES_NOT_EXIST_ERROR, INVALID_REFERENCE_TYPE_ERROR
from tests.testcases import INPRO_VALID1, INPRO_VALID2, INPRO_VALID2, TECHREPORT_VALID, ARTICLE_VALID, PHD_VALID
from database_connection import get_database_connection


VALID_FILE_NAME = "data/valid_file_name.bib"


class TestReference(unittest.TestCase):
    """Tests for reference repository class """

    def setUp(self):
        self.repository = ReferenceRepository()
        self.repository.empty_all_tables()
        self.inpro_all = INPRO_VALID1
        self.test_ref1 = INPRO_VALID2
        self.test_ref2 = TECHREPORT_VALID
        self.test_ref3 = ARTICLE_VALID
        self.test_ref4 = PHD_VALID

        if os.path.exists(VALID_FILE_NAME):
            os.remove(VALID_FILE_NAME)

    def test_loading_references_from_empty_gives_correct_amount(self):
        """Tests that initially the list containing references
        is empty
        """
        references = self.repository.load_all()
        self.assertEqual(len(references), 0)

    def test_loading_one_from_empty_raises_error(self):
        """Test for loading one reference when there are none"""
        with pytest.raises(ValueError,
                           match=KEY_DOES_NOT_EXIST_ERROR):
            self.repository.load_one("test_key")

    def test_loading_one_with_incorrect_key_raises_error(self):
        """Test for loading one reference when key is wrong"""
        self.repository.save(self.inpro_all)
        with pytest.raises(ValueError,
                           match=KEY_DOES_NOT_EXIST_ERROR):
            self.repository.load_one("Key321")

    def test_loading_one_returns_reference_object(self):
        """Test succesfull retrieval"""
        self.repository.save(self.inpro_all)
        reference = self.repository.load_one("Garcia23")
        assert issubclass(type(reference), Reference)

    def test_save_to_db(self):
        """Adds 4 references and checks that database has 
        4 more records"""
        self.repository.save(self.test_ref1)
        self.repository.save(self.test_ref2)
        self.repository.save(self.test_ref3)
        self.repository.save(self.test_ref4)

        refs_after_add = self.repository.load_all()
        self.assertEqual(len(refs_after_add), 4)

    def test_non_existent_key_returns_valueerror(self):
        with pytest.raises(ValueError,
                           match=KEY_DOES_NOT_EXIST_ERROR):
            self.repository.load_one("NON-EXISTENT")

    def test_delete_from_database(self):
        self.repository.save(self.test_ref1)
        self.repository.save(self.test_ref2)
        refs_after_add = self.repository.load_all()
        key = refs_after_add[0].key
        self.repository.delete_from_db(key)
        refs_after_delete = self.repository.load_all()
        self.assertEqual(len(refs_after_delete)+1, len(refs_after_add))
        key2 = refs_after_add[1].key
        self.repository.delete_from_db(key2)
        refs_after_delete2 = self.repository.load_all()
        self.assertEqual(len(refs_after_delete2)+2, len(refs_after_add))

    def test_save_to_file_with_invalid_path_raises_error(self):
        with pytest.raises(FileNotFoundError):
            self.repository.save_to_file("../invalid_path/file")

    def test_save_to_file_with_valid_path_creates_file(self):
        self.repository.save(self.test_ref1)
        self.repository.save_to_file(VALID_FILE_NAME)
        self.assertTrue(os.path.exists(VALID_FILE_NAME))
        if os.path.exists(VALID_FILE_NAME):
            os.remove(VALID_FILE_NAME)

    def test_non_supported_entry_type_raises_error(self):
        """Add directely to SQL database reference type_id
        not supported by program, and ensure that correct
        value error is raised"""
        connection = get_database_connection()
        cursor = connection.cursor()
        sql = """INSERT INTO Bibrefs (key, title, author_id, year, referencetype_id)
                VALUES ("Author23", "Title", 999, 2023, 999)
            """
        cursor.execute(sql)
        connection.commit()
        with pytest.raises(ValueError, match=INVALID_REFERENCE_TYPE_ERROR):
            self.repository.load_one("Author23")
