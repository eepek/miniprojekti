""" Module containing GUI notify screen

    Yields:
        Screen: Textual widget
    """

from textual.app import ComposeResult
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Grid


class NotifyScreen(ModalScreen[bool]):
    """Screen shows success or error
    """

    def __init__(self, result) -> None:
        super().__init__()
        self.result = result
        self.ok = Button("Ok", id="ok")

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.result),
            self.ok
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Method processing action from
        button pressed.

        Args:
            event (Button.Pressed): Textual button pressed message
        """
        if event.button.id == "ok":
            self.dismiss(True)

    BINDINGS = [("enter, ctrl+j", "close", "Close")]

    def action_close(self):
        """Action on Yes button selected
        """
        self.dismiss(True)

    def on_key(self, key: Key):
        """Tracks if Enter button presses happen on focused
        button"""
        if key.key in ["enter", "ctrl+j"]:
            if self.ok.has_focus:
                self.dismiss(True)
