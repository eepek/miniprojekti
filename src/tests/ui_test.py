"""Unittests for UI module."""
import unittest
from collections import deque
from typing import List
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from ui import UI
from constants import ROOT_DIR, UNSUITABLE_COMMAND_ERROR, FIELD_MANDATORY_ERROR, YEAR_FORMAT_ERROR

class MockIO:
    """Class to mock IO.

    This class allows to replace standard console IO with a predetermined list
    of commands and get the output as a string.

    Args:
        command_list (List[str]): list of strings to feed to the program in order
    """
    def __init__(self, command_list: List[str]) -> None:
        self.command_list = deque(command_list)
        self.output = ""

    def read(self, prompt: str) -> str:
        """Return next input from the command list.
        
        Also write the prompt to the output.
        """
        self.output += "\n" + prompt
        if len(self.command_list) == 0:
            # If you don't give the exit command, this handles it.
            raise SystemExit
        return self.command_list.popleft()

    def write(self, text: str) -> None:
        "Write text to the output."
        self.output += "\n" + text

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
        with self.assertRaises(SystemExit):
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
            ""
        ]
        output = self.run_program(command_list)
        self.assertIn(FIELD_MANDATORY_ERROR, output)

    def test_validation_error(self):
        """Test that an invalid field prints a validation error."""
        command_list = [
            "2", # command
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
