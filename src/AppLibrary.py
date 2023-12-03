"""Module for the library class for the Robot framework."""
from mock_io import MockIO
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from ui import UI

class AppLibrary:
    """Library class for the Robot framework."""
    def __init__(self):
        self._io = MockIO()
        self._ref_repository = ReferenceRepository()
        self._ref_repository.empty_all_tables()
        self._ref_services = ReferenceServices(self._ref_repository)
        self._ui = UI(self._io, self._ref_repository, self._ref_services)

    def command(self, value):
        """Add command to be executed."""
        self._io.add_command(value)

    def run_program(self):
        """Start running the program with the predetermined command list."""
        self._ui.start()

    def output_should_contain(self, string: str):
        """Assert that the output contains a string."""
        output = self._io.output
        if string not in output:
            raise AssertionError(f"Output {string} not in output {output}:")
