"""Unittests for UI module."""
import unittest
from typing import List
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from entities.reference import ReferenceType
from ui import UI
from mock_io import MockIO
from constants import ROOT_DIR, UNSUITABLE_COMMAND_ERROR, FIELD_MANDATORY_ERROR, YEAR_FORMAT_ERROR, KEY_DOES_NOT_EXIST_ERROR


class TestUI(unittest.TestCase):
    """Unittests for UI class."""

    def setUp(self):
        self.ref_repository = ReferenceRepository(f"{ROOT_DIR}/tests/test_references.bib")
        self.ref_repository.empty_all_references()
        self.ref_services = ReferenceServices(self.ref_repository)

    def run_program(self, command_list: List[str]) -> str:
        """Run the program with a command list.

        Args:
            command_list (List[str]): list of commands to run in order

        Returns:
            str: the output string of the program including newline characters
        """
        mock_io = MockIO(command_list)
        ui = UI(mock_io, self.ref_repository, self.ref_services)
        ui.start()
        return mock_io.output

    def test_shutting_down(self):
        """Test shutting down the program."""
        command_list = [
            "x"
        ]
        output = self.run_program(command_list)
        self.assertIn("Shutting down", output)

    def test_adding_reference(self):
        """Test adding a reference (Inproceeding)."""
        command_list = [
            "2", # command
            "inproceedings", # type
            "key_value", # key
            "title_value", # title
            "author_value", # author
            "booktitle_value", #booktitle
            "2000", #year
            "", # editor
            "", # volume
            "", # series
            "", # pages
            "", # address
            "", # month
            "", # note
            "1", # command
            "x", # command
        ]
        output = self.run_program(command_list)
        self.assertIn("{author_value}", output)

    def test_invalid_command(self):
        """Test entering an invalid command."""
        command_list = [
            "wrong",
            "x"
        ]
        output = self.run_program(command_list)
        self.assertIn(UNSUITABLE_COMMAND_ERROR, output)

    def test_show_commands(self):
        """Test showing all commands."""
        command_list = [
            "c",
            "x"
        ]
        output = self.run_program(command_list)
        self.assertEqual(output.count("Command options:"), 2)

    def test_field_mandatory(self):
        """Test that an empty string on a mandatory field gives an error."""
        command_list = [
            "2",
            "inproceedings",
            ""
        ]
        output = self.run_program(command_list)
        self.assertIn(FIELD_MANDATORY_ERROR, output)

    def test_validation_error(self):
        """Test that an invalid field prints a validation error."""
        command_list = [
            "2", # command
            "inproceedings", # type
            "key_value", # key
            "title_value", # title
            "author_value", # author
            "booktitle_value", #booktitle
            "invalid", #year
            "", # editor
            "", # volume
            "", # series
            "", # pages
            "", # address
            "", # month
            "", # note
            "x", # command
        ]
        output = self.run_program(command_list)
        self.assertIn(YEAR_FORMAT_ERROR, output)
    
    def test_show_all_reference_keys(self):
        """Test showing all reference keys."""
        command_list = [
            "3",
            "x",
            "x"
        ]
        fields = {"title":"test title","author":"test author","booktitle":"test_title", "year":1995}
        self.ref_services.create_reference(ReferenceType.INPROCEEDINGS, fields)
        self.ref_services.create_reference(ReferenceType.INPROCEEDINGS, fields)
        output = self.run_program(command_list)
        self.assertEqual(output.count("testaut95"), len(self.ref_repository._references))

    def test_show_reference_by_key(self):
        """Test accessing single reference via ui"""
        command_list = [
            "3",
            "k",
            "testaut95",
            "x",
            "x"
        ]
        fields = {"title":"test title","author":"test author","booktitle":"test title", "year":1995}
        expected_output = "@inproceedings{testaut95,\n"\
                        "    title        = {test title},\n"\
                        "    author       = {test author},\n"\
                        "    booktitle    = {test title},\n"\
                        "    year         = 1995\n"\
                        "}"
        self.ref_services.create_reference(ReferenceType.INPROCEEDINGS, fields)
        self.ref_services.create_reference(ReferenceType.INPROCEEDINGS, fields)
        output = self.run_program(command_list)
        self.assertIn(expected_output, output)

    def test_show_reference_by_invalid_key(self):
        """Test for raising error if key does not exist"""
        command_list = [
            "3",
            "invalid_key"
        ]
        output = self.run_program(command_list)
        print(output)
        self.assertIn(KEY_DOES_NOT_EXIST_ERROR, output)
