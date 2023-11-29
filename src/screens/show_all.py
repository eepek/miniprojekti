"""Module containing GUI screen to show all
the references, currently in BibTex form,
but will be modified to show more user friendly
output

    Yields:
        Screen: Textual Widget
    """
from textual.app import ComposeResult
from textual.widgets import Footer, Label
from textual.containers import Center
from textual.screen import Screen


class ShowAll(Screen[None]):
    """Screen that shows all references in
    BibTex style"""

    def __init__(self, references) -> None:
        super().__init__()
        self.references = [Label(str(ref)) for ref in references]

    BINDINGS = [("b", "back", "Back")]

    def compose(self) -> ComposeResult:
        textfile = Center(*self.references)
        yield textfile
        yield Footer()

    def action_back(self):
        """Closes the screen and goes back to previous
        triggered by keystroke"""
        self.app.pop_screen()
