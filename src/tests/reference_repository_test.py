"""Unittests for reference module"""
import unittest
from repositories.reference_repository import ReferenceRepository
from entities.reference import Inproceedings
from constants import ROOT_DIR


class TestReference(unittest.TestCase):
    """Tests for reference repository class """

    def setUp(self):
        self.repository = ReferenceRepository(f"{ROOT_DIR}/tests/test_references.bib")
        self.repository.empty_all_references()
        self.repository.init_references()
        self.inpro_all = Inproceedings(
            key="Key123",
            title="Inproceeding name",
            author="Mikki Hiiri",
            booktitle="Proceedings of the Conference",
            year=2023,
            volume="1",
            pages="123-145",
            address="Helsinki",
            month="June",
            note="test")

    def test_saving_reference_work(self):
        """Testing that after adding self.inpro_all Inproceedings
        object to references file, file is 12 lines longer
        """
        before_lines = self.repository.file_lines()

        self.repository.save(self.inpro_all)

        after_lines = self.repository.file_lines()

        self.assertEqual(before_lines + 12, after_lines)

    def test_loading_references_from_empty_gives_correct_amount(self):
        """Tests that initially the list containing references
        is empty
        """
        references = self.repository.load_all()
        self.assertEqual(len(references), 0)

    def test_after_saving_reference_list_is_updated(self):
        """Tests that after adding reference it is found
        in file and in list"""

        self.repository.save(self.inpro_all)
        lines = self.repository.file_lines()
        self.assertEqual(12, lines)

        reference_list = self.repository.load_all()

        self.assertEqual(1, len(reference_list))
