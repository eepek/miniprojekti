"""Module with class to mock IO"""
from collections import deque
from typing import List

class MockIO:
    """Class to mock IO.

    This class allows to replace standard console IO with a predetermined list
    of commands and get the output as a string.

    Args:
        command_list (List[str]): list of strings to feed to the program in order
    """
    def __init__(self, command_list: List[str] = []) -> None:
        self.command_list = deque(command_list)
        self.output = ""

    def read(self, prompt: str) -> str:
        """Return next input from the command list.
        
        Also write the prompt to the output.
        """
        self.output += "\n" + prompt
        if len(self.command_list) > 0:
            return self.command_list.popleft()

    def write(self, text: str) -> None:
        "Write text to the output."
        self.output += "\n" + text
        print(self.output)
    
    def add_input(self, input: str):
        self.command_list.append(input)
        print("input added", input)
