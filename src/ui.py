from cli_io import ConsoleIO
from repositories.reference_repository import ReferenceRepository
from services.refrence_services import ReferenceServices


class UI():
    def __init__(self, io: ConsoleIO, reference_repository: ReferenceRepository,
                 reference_service: ReferenceServices):
        self._io = io
        self._reference_repository = reference_repository
        self._reference_services = reference_service
        self.commands = {
            "1": "Browse all references ",
            "2": "Add reference (inproceedings)",
            "c": "Show command options",
            "x": "Exit"
            # more commands added when needed
        }

        # temporary greeding, we need a name for the app
        self._io.write("Welcome to your vault of references!")

    def start(self):
        self.show_commands()

        while True:
            self._io.write("\nTo view command options, type c")
            command = self._io.read("What would you like to do?: ")

            if command not in self.commands:
                self._io.write("Error: Unsuitable command")

            if command == "1":
                self.show_inproceedings()

            if command == "2":
                self.add_inproceedings()

            if command == "c":
                self.show_commands()

            if command == "x":
                self.exit()

    def show_commands(self):
        self._io.write("\nCommand options:\n")
        for key, value in self.commands.items():
            command = f"{key}: {value}"
            self._io.write(command)

    def add_inproceedings(self):

        reference = self._io.read("\nAdd reference: ")  # temporary
        if reference:
            # Tässä sit kun saadaan kaikki tiedot kerättyä niin kutsutaan referencerepositorya
            self._reference_services.create_reference(reference)
            # tai jos/kun halutaan checkata user inputit niin
            # joku reference_service luokka joka tekee
            # checkit ja sen jälkeen kutsuu reference repositorya
            self._io.write(f"\n{reference} added succesfully")
        else:
            # this is not the final error message
            self._io.write("\nError: Something went wrong")

    def show_inproceedings(self):
        for reference in self._reference_repository.load_all():
            self._io.write(str(reference))

    def exit(self):
        self._io.write("\nShutting down")
        exit()
