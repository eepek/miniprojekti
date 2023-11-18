from cli_io import ConsoleIO

class UI():
    def __init__(self, io: ConsoleIO):
        self._io = io
        self.commands= {
            "1" : "Browse all references ",
            "2" : "Add reference (inproceedings)",
            "c" : "Show command options",
            "x" : "Exit"
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
                self._io.write("this function is under construction")

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

        reference = self._io.read("\nAdd reference: ") #temporary
        if reference:
            #adding the reference

            self._io.write("\nReference added succesfully")
        else:
            self._io.write("\nError: Something went wrong")# this is not the final error message

    def exit(self):
        self._io.write("\nShutting down")
        exit()
