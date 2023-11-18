"""Module which contains functions needed for reading
  user input and printing out info for user

  Returns:
      String: User input
  """
class ConsoleIO:
    """Class which reads inputs from the user
  and prints out values for user to see
  """

    def read(self, prompt):
        """Reads input the user gives

        Args:
            prompt (string): Prompt that is given to trigger user input

        Returns:
            String: User input
        """

        return input(prompt)

    def write(self, text):
        """Prints information for the user

        Args:
            text (String): Text that is printed for user to view
        """
        print(text)
