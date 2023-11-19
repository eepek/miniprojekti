from ui import UI
from cli_io import ConsoleIO
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices


def main():
    _io = ConsoleIO()
    _reference_repository = ReferenceRepository("./data/references.bib")
    # Injektoidaan ReferenceRepository sekä serviceille että UI:lle
    _reference_services = ReferenceServices(_reference_repository)
    program = UI(_io, _reference_repository, _reference_services)
    program.start()


if __name__ == "__main__":
    main()
