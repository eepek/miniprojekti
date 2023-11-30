"""Module containing screens related to
    listing references by key and showing single
    reference

    Yields:
        _type_: _description_
    """
from textual import on, events
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, OptionList, DataTable, TextArea, RichLog
from textual.widgets.option_list import Option
from textual.containers import Center
from textual.screen import Screen
from textual.reactive import reactive
from entities.reference import Reference
from screens.confirmation_screen import ConfirmationScreen
from screens.notify_screen import NotifyScreen


class ListKeys(Screen[None]):
    """Screen that lists all references in an optionlist
    showing reference keys

    Args:
        Screen (Screen): Textual Screen component
    """

    def __init__(self, references: list[Reference], delete_reference, create_reference) -> None:
        super().__init__()
        self.references = references
        self.option_items = [Option(ref.key, id=ref.key)
                             for ref in references]
        self.delete_reference = delete_reference
        self.create_reference = create_reference
        self.option_id = 0

    BINDINGS = [("b", "back", "Back"),
                ("enter, ctrl+j", "open_option", "Open", )]

    def compose(self) -> ComposeResult:
        yield Center(OptionList(*self.option_items, id="optionList"))
        yield Footer()
        yield RichLog()

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
            self.references, self.option_id, self.delete_reference))

    def action_back(self):
        """Closes screen, triggered by keystroke"""
        self.app.pop_screen()


class SingleReference(Screen[None]):
    """Screen containing a single reference."""
    CSS_PATH = "style.tcss"

    BINDINGS = [("d", "delete_reference", "Delete"),
                ("b", "back", "Back")]

    def __init__(self, references: list, reference_id: int, delete_reference) -> None:
        super().__init__()
        self.reference: Reference = references[reference_id]
        self.delete_reference = delete_reference

    def compose(self) -> ComposeResult:
        yield SingleReferenceWidget(self.reference)
        yield RichLog()
        yield Footer()

    def action_back(self):
        """Method that closes screen,
        triggered by key press.
        """
        self.app.pop_screen()

    def action_delete_reference(self):
        """Calls for deletion of current
        reference from DB"""
        # Tähän varmaan joku confirmation ois hyvä?
        def confirm(confirmation):
            if confirmation:
                answer = self.delete_reference(self.reference.key)
                if answer:
                    def close(confirm: bool):
                        if confirm:
                            self.app.pop_screen()

                    self.app.push_screen(NotifyScreen(
                        f"{self.reference.key} succesfully removed from DB"), close)
                else:
                    self.app.push_screen(NotifyScreen(
                        "Error, could not delete reference"))

        self.app.push_screen(ConfirmationScreen('delete this entry'), confirm)


class SingleReferenceWidget(Widget):
    """Widget for displaying a single reference."""
    # (row_index, key, value)
    modify_field: tuple | None = reactive(None)

    def __init__(self, reference) -> None:
        super().__init__(classes="single-ref")
        self.reference: Reference = reference
        self.last_selected_coord = None

    def compose(self) -> ComposeResult:
        table = DataTable()
        table.add_column(self.reference.reference_type.value, width=15)
        table.add_column(self.reference.key)
        for field, value in self.reference.fields.items():
            table.add_row(field, value)
        yield table

        t = TextArea(classes="modify-field")
        t.show_line_numbers = False
        t.visible = False
        yield t

    def watch_modify_field(self, new: tuple | None):
        """If the modify_field variable changes, this function will be called with the new value.

        This will open/close the field modify input.
        """
        field = self.query_one(TextArea)
        if new is None:
            field.visible = False
        else:
            field = self.query_one(TextArea)
            field.styles.margin = (self.modify_field[0] + 1, 0, 0, 17)
            field.load_text(self.modify_field[2])
            field.visible = True
            field.focus()
            field.move_cursor(field.get_cursor_line_end_location())

    @on(DataTable.CellSelected)
    def cell_selected(self, event: DataTable.CellSelected):
        """This will be called when the mouse clicks on a cell.

        If the click is on a cell, which was already selected, open the field modify input.
        """
        table = self.query_one(DataTable)
        if event.coordinate == self.last_selected_coord and event.coordinate.column == 1 \
                and self.modify_field is None:
            row = table.cursor_coordinate.row
            field, value = table.get_row_at(row)
            self.modify_field = (row, field, value)
        self.last_selected_coord = event.coordinate

    @on(DataTable.CellHighlighted)
    def cell_highlighted(self):
        """If clicked on another cell, close field modify input."""
        self.modify_field = None

    def on_key(self, event: events.Key):
        """This will detect whether to open/close the field modify input,
        or to send new modified value.
        """
        table = self.query_one(DataTable)
        if event.key == "ctrl+j" and self.modify_field is not None:
            field = self.query_one(TextArea)
            try:
                self.app.reference_services.validate_field(self.modify_field[1], field.text)
                self.notify("New value: " + field.text)
                # Implement saving field here
                self.modify_field = None
            except ValueError as error:
                self.notify(f"Error: {error}", severity="error")
        elif event.key == "ctrl+j" and table.cursor_coordinate.column == 1 \
                and self.modify_field is None:
            row = table.cursor_coordinate.row
            field, value = table.get_row_at(row)
            self.modify_field = (row, field, value)
        if event.key == "escape":
            self.modify_field = None
