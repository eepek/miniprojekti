""" Module containing GUI confirmation screen

    Yields:
        Screen: Textual widget
    """

from textual.app import ComposeResult
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Grid


class ConfirmationScreen(ModalScreen[bool]):
    """Screen to confirm user wants
    to proceed with action. Returns Boolean,
    True if yes, False if No
    """

    def __init__(self, action) -> None:
        super().__init__()
        self.action = action
        self.yes = Button("Yes", variant="primary", id="yes")
        self.no = Button("No", variant="error", id="no")

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"Do you want to {self.action}", id="question"),
            self.yes,
            self.no,
            id="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Method processing action from
        button pressed.

        Args:
            event (Button.Pressed): Textual button pressed message
        """
        if event.button.id == "yes":
            self.action_yes()
        else:
            self.action_no()

    BINDINGS = [("y", "yes", "Yes"),
                ("n", "no", "no")]

    def action_yes(self):
        """Action on Yes button selected
        """
        self.dismiss(True)

    def action_no(self):
        """Action on No button selected"""
        self.dismiss(False)

    def on_key(self, key: Key):
        """Tracks if Enter button presses happen on focused
        button"""
        if key.key in ["enter", "ctrl+j"]:
            if self.yes.has_focus:
                self.action_yes()
            elif self.no.has_focus:
                self.action_no()
