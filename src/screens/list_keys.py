"""Module containing screens related to
    listing references by key and showing single
    reference

    Yields:
        _type_: _description_
    """
from textual import on
from textual.app import ComposeResult
from textual.widgets import Footer, OptionList, Label
from textual.widgets.option_list import Option
from textual.containers import Center
from textual.screen import Screen
from entities.reference import Reference


class ListKeys(Screen[None]):
    """Screen that lists all references in an optionlist
    showing reference keys

    Args:
        Screen (Screen): Textual Screen component
    """

    def __init__(self, references: list[Reference]) -> None:
        super().__init__()
        self.references = references
        self.option_items = [Option(ref.key, id=ref.key)
                             for ref in references]
        self.option_id = 0

    BINDINGS = [("b", "back", "Back"),
                ("enter, ctrl+j", "open_option", "Open", )]

    def compose(self) -> ComposeResult:
        yield Center(OptionList(*self.option_items, id="optionList"))
        yield Footer()

    @on(OptionList.OptionMessage)
    def user_selected(self, event: OptionList.OptionSelected):
        """Identifies id for current option selected
        by user

        Args:
            event (OptionList.OptionSelected): Textual message
        """
        self.option_id = event.option_index

    def action_open_option(self):
        """Opens new screen from selected option,
        triggered by key stroke
        """
        self.app.switch_screen(SingleReference(
            self.references, self.option_id))

    def action_back(self):
        """Closes screen, triggered by keystroke"""
        self.app.pop_screen()


class SingleReference(Screen[None]):
    """Screen class that shows a single reference
    view to the user

    Args:
        Screen (Screen): Textual Screen component
    """

    def __init__(self, references, reference_id) -> None:
        super().__init__()
        self.reference = references[reference_id]

    BINDINGS = [("e", "edit_reference", "Edit"),
                ("d", "delete_reference", "Delete"),
                ("b", "back", "Back")]

    def compose(self) -> ComposeResult:
        yield Center(Label(str(self.reference)), id="dialog")
        yield Footer()

    def action_back(self):
        """Method that closes screen,
        triggered by key press.
        """
        self.app.pop_screen()
