"""Main program module."""
from ui import UI
from gui import GUI
from cli_io import ConsoleIO
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from constants import ROOT_DIR


def main():
    """Main program function."""
    _data_folder = f"{ROOT_DIR}/data/references.bib"
    _reference_repository = ReferenceRepository(_data_folder)
    # Injektoidaan ReferenceRepository sekä serviceille että UI:lle
    _reference_services = ReferenceServices(_reference_repository)
    program = GUI(_reference_repository, _reference_services)
    program.run()


if __name__ == "__main__":
    main()
