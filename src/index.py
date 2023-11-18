from ui import UI
from cli_io import ConsoleIO

def main():
    _io = ConsoleIO()
    program = UI(_io)
    program.start()


if __name__ == "__main__":
    main()
