"""Unittests for reference module"""
import unittest
import pytest
from repositories.reference_repository import ReferenceRepository, ReferenceType
from entities.reference import Reference
from constants import KEY_DOES_NOT_EXIST_ERROR


class TestReference(unittest.TestCase):
    """Tests for reference repository class """

    def setUp(self):
        self.repository = ReferenceRepository()
        self.repository.empty_all_tables()
        self.inpro_all = Reference(ReferenceType.INPROCEEDINGS, "Key123", {
            "title": "Inproceeding name",
            "author": "Mikki Hiiri",
            "booktitle": "Proceedings of the Conference",
            "year": 2023,
            "volume": 1,
            "pages": "123-145",
            "address": "Helsinki",
            "month": "June",
            "note": "test"
        })
        self.test_ref1 = Reference(ReferenceType.INPROCEEDINGS, "Unique1", {
            "title": "Test title",
            "author": "One, Some",
            "booktitle": "Annual conference of Everything",
            "year": 2021,
            "volume": 2,
            "pages": "111-145",
            "address": "Stockholm",
            "month": "June",
            "note": "test note"
        })
        self.test_ref2 = Reference(ReferenceType.TECHREPORT, "Unique2", {
            "title": "Test title",
            "author": "Body, Some",
            "institution": "important place",
            "year": 2022,
            "type": "Whitepaper",
            "address": "Tanska",
            "month": "7",
            "note": "test note"
        })

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
        reference = self.repository.load_one("Key123")
        assert issubclass(type(reference), Reference)

    def test_save_to_db(self):
        init_refs = self.repository.load_all_from_database()
        self.repository.save_to_db(self.test_ref1)
        self.repository.save_to_db(self.test_ref2)

        refs_after_add = self.repository.load_all_from_database()
        self.assertEqual(len(refs_after_add), 2)

    def test_non_existent_key_returns_valueerror(self):
        with pytest.raises(ValueError,
                           match=KEY_DOES_NOT_EXIST_ERROR):
            self.repository.load_one_from_database("NON-EXISTENT")

    def test_delete_from_database(self):
        init_refs = self.repository.load_all_from_database()
        self.repository.save_to_db(self.test_ref1)
        self.repository.save_to_db(self.test_ref2)
        refs_after_add = self.repository.load_all_from_database()
        key = refs_after_add[0].key
        self.repository.delete_from_db(key)
        refs_after_delete = self.repository.load_all_from_database()
        self.assertEqual(len(refs_after_delete)+1, len(refs_after_add))
        key2 = refs_after_add[1].key
        self.repository.delete_from_db(key2)
        refs_after_delete2 = self.repository.load_all_from_database()
        self.assertEqual(len(refs_after_delete2)+2, len(refs_after_add))
