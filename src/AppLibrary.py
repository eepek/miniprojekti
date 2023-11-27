from mock_io import MockIO
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from constants import ROOT_DIR
from ui import UI

class AppLibrary:
    def __init__(self):
        self._io = MockIO()
        self._ref_repository = ReferenceRepository(f"{ROOT_DIR}/tests/test_references.bib")
        self._ref_repository.empty_all_references()
        self._ref_services = ReferenceServices(self._ref_repository)
        self._ui = UI(self._io, self._ref_repository, self._ref_services)
    
    def command(self, value):
        self._io.add_input(value)
    
    def run_program(self):
        self._ui.start()
