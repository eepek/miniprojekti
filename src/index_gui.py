"""Main program module."""
from tkinter import filedialog
from gui import GUI
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices


def main():
    """Main program function."""
    _reference_repository = ReferenceRepository()
    # Injektoidaan ReferenceRepository sekä serviceille että UI:lle
    _reference_services = ReferenceServices(_reference_repository)
    program = GUI(_reference_repository, _reference_services, filedialog)
    program.run()


if __name__ == "__main__":
    main()
