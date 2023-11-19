"""Unittests for reference module"""
import unittest
from repositories.reference_repository import ReferenceRepository
from entities.reference import Inproceedings


class TestReference(unittest.TestCase):
    """Tests for reference repository class """

    def setUp(self):
        self.repository = ReferenceRepository("src/tests/test_references.bib")
        self.repository.empty_all_references()
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

    def test_loading_references_gives_correct_amount(self):
        """Tests that initially the list containing references
        is empty
        """
        references = self.repository.load_all()
        self.assertEqual(len(references), 0)
