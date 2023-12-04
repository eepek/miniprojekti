"""Module containing GUI screen to show all
the references, currently in BibTex form,
but will be modified to show more user friendly
output

    Yields:
        Screen: Textual Widget
    """
from textual.app import ComposeResult
from textual.widgets import Footer, DataTable
from textual.screen import Screen


class ShowAll(Screen[None]):
    """Screen that shows all references in
    BibTex style"""

    def __init__(self, references) -> None:
        super().__init__(classes="showall")
        self.references = references
    BINDINGS = [("escape", "back", "Back"),
                ("up", "scroll_up", "Move cursor up"),
                ("down", "scroll_down", "Move cursor down")]

    def compose(self) -> ComposeResult:
        if len(self.references) > 0:
            for ref in self.references:
                table = DataTable(show_cursor=False)
                table.add_column(ref.reference_type.value, width=15)
                table.add_column(ref.key)
                for field, value in ref.fields.items():
                    if value is None:
                        continue
                    table.add_row(field, str(value))
                table.add_row("", "")
                yield table
        yield Footer()

    def action_back(self):
        """Closes the screen and goes back to previous
        triggered by keystroke"""
        self.app.pop_screen()

    def action_scroll_down(self) -> None:
        self.scroll_down()

    def action_scroll_up(self) -> None:
        self.scroll_up()
