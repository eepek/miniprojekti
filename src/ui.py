"""Module for the command line user interface"""
import sys
from cli_io import ConsoleIO
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from constants import INPROCEEDINGS_KEYS, INPROCEEDINGS_MANDATORY_KEYS, \
    FIELD_MANDATORY_ERROR, UNSUITABLE_COMMAND_ERROR

class UI():
    """Class that creates a command line user interface to the program.

    Args:
        io (ConsoleIO): class to write and read from the console
        reference_repository (ReferenceRepository): class to store References
        reference_service (ReferenceService): class to create References
    """
    def __init__(self, io: ConsoleIO, reference_repository: ReferenceRepository,
                 reference_service: ReferenceServices):
        self._io = io
        self._reference_repository = reference_repository
        self._reference_services = reference_service
        self.commands = {
            "1": "Browse all references",
            "2": "Add reference (inproceedings)",
            "3": "View references by key",
            "c": "Show command options",
            "x": "Exit"
            # more commands added when needed
        }

        # temporary greeding, we need a name for the app
        self._io.write("Welcome to your vault of references!")

    def start(self):
        """Start an interactive command line session to ask the user for commands."""
        self.show_commands()

        while True:
            self._io.write("\nTo view command options, type c")
            command = self._io.read("What would you like to do?: ")

            if command not in self.commands:
                self._io.write("Error: " + UNSUITABLE_COMMAND_ERROR)

            if command == "1":
                self.show_references()

            if command == "2":
                self.add_inproceedings()

            if command == "3":
                self.show_reference_by_key()

            if command == "c":
                self.show_commands()

            if command == "x":
                self.exit()

    def show_commands(self) -> None:
        """Print command options."""
        self._io.write("\nCommand options:\n")
        for key, value in self.commands.items():
            command = f"{key}: {value}"
            self._io.write(command)

    def get_field(self, field: str, mandatory: bool) -> str:
        """Start an interactive command line session to ask the user for
        a field value.

        Args:
            field (str): the field name to ask the value for
            mandatory (bool): whether to insist for a value, or allow skipping
        
        Returns:
            str: value for field
        """
        mandatory_text = ""

        if mandatory:
            mandatory_text = "mandatory"
        else:
            mandatory_text = "optional, enter to skip"

        while True:
            if field == "author":
                value = self._io.read(
                    f"Enter value for field {field} (Lastname, Firstname) ({mandatory_text}): "
                    )
            else:
                value = self._io.read(f"Enter value for field {field} ({mandatory_text}): ")
            if value == "":
                if mandatory:
                    self._io.write(f"Error: {field}: " + FIELD_MANDATORY_ERROR)
                else:
                    return ""
            else:
                try:
                    self._reference_services.validate_field(field, value)
                    return value
                except ValueError as validation_error:
                    self._io.write(f"Validation Error for {field}: {str(validation_error)}")

    def add_inproceedings(self) -> None:
        """Start an interactive command line session to ask the user for
        field values for an Inproceedings-reference.

        Calls reference_services.create_reference with field values.
        """
        field_values = {}

        for field in INPROCEEDINGS_KEYS:
            mandatory = field in INPROCEEDINGS_MANDATORY_KEYS
            value = self.get_field(field, mandatory)

            if value != "":
                field_values[field] = value
        try:
            self._reference_services.create_reference(field_values)
        except ValueError as error:
            self._io.write("Error: " + str(error))

    def show_references(self) -> None:
        """Print references."""
        for reference in self._reference_repository.load_all():
            self._io.write(str(reference))

    def show_one_reference(self, key: str) -> None:
        """Print one reference with given key
        Args:
            key (String): Reference key
        """
        reference = self._reference_repository.load_one(key)
        self._io.write(f"\n{str(reference)}")

    def show_all_reference_keys(self) -> None:
        """Print all keys"""
        self._io.write("Keys:")
        for reference in self._reference_repository.load_all():
            self._io.write(f"   {reference.key}")

    def show_reference_by_key(self) -> None:
        """Loop for viewing references by key"""
        self.show_all_reference_keys()
        while True:
            key = self._io.read("\nEnter key, 'k' for keys or 'x' for return: ")
            if key == "x":
                return
            if key == "k":
                self.show_all_reference_keys()
            else:
                try:
                    self.show_one_reference(key)
                except ValueError as error:
                    self._io.write("Error: " + str(error))

    def exit(self):
        """Exit program."""
        self._io.write("\nShutting down")
        sys.exit()
