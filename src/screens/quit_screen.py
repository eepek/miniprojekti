""" Module containing GUI quit-screen

    Yields:
        Screen: Textual widget
    """

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Footer
from textual.containers import Grid


class QuitScreen(Screen):
    """Screen that is shown when user
    wants to exit the application
    Args:
        Screen (Screen): Textual Screen component

    Yields:
        Grid: Grid containing quit and cancel buttons
        Footer: Bottom footer showing key commands
    """
    BINDINGS = [("q", "exit", "Quit"),
                ("c", "cancel", "Cancel"),
                ("enter, ctrl+j", "on_button_pressed")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Do you want to exit the application?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Method processing action from
        button pressed.

        Args:
            event (Button.Pressed): Textual button pressed message
        """
        if event.button.id == "quit":
            self.action_exit()
        else:
            self.action_cancel()

    def action_exit(self):
        """Method that closes application,
        triggered by key press
        """
        self.app.exit()

    def action_cancel(self):
        """Method that cancels quit screen,
        triggered by key press
        """
        self.app.pop_screen()
