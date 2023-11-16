class UI:
    def __init__(self):
        self.commands= {
            "1" : "Browse all references ",
            "2" : "Add reference (inproceedings)",
            "c" : "Show command options",
            "x" : "Exit"
            # more commands added when needed
        }
        
        # temporary greeding, we need a name for the app
        print("Welcome to your vault of references!")

        self.start()


    def start(self):
        self.show_commands()

        while True: 
            print("\nTo view command options, type c")
            command = input("What would you like to do?: ")


            if command not in self.commands:
                print("Error: Unsuitable command")

            if command == "1":
                print("this function is under construction")

            if command == "2":
                self.add_inproceedings()

            if command == "c":
                self.show_commands()

            if command == "x":
                self.exit()
    

    def show_commands(self):
        print("\nCommand options:\n")
        for key, value in self.commands.items():
            print(key,value)


    def add_inproceedings(self):

        reference = input("\nAdd reference: ") #temporary
        if reference:
            #adding the reference

            print("\nReference added succesfully")
        else:
            print("\nError: Something went wrong")# this is not the final error message

    def exit(self):
        print("\nShutting down")
        exit()
