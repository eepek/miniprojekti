"""Module containing screens related to
    listing references by key and showing single
    reference

    Yields:
        _type_: _description_
    """
import sqlite3
from textual import on, events
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, OptionList, DataTable, TextArea, RichLog, Header
from textual.widgets.option_list import Option
from textual.containers import Center
from textual.screen import Screen
from textual.reactive import reactive
from textual.coordinate import Coordinate
from textual.events import Key
from textual.message import Message
from entities.reference import Reference
from screens.confirmation_screen import ConfirmationScreen


class ListKeys(Screen[None]):
    """Screen that lists all references in an optionlist
    showing reference keys

    Args:
        Screen (Screen): Textual Screen component
    """

    def __init__(self, references: list[Reference], delete_reference, create_reference) -> None:
        super().__init__()
        self.sub_title = "List by key"
        self.references = references
        self.option_items = [Option(ref.key, id=ref.key)
                             for ref in references]
        self.delete_reference = delete_reference
        self.create_reference = create_reference
        self.option_id = 0

    BINDINGS = [("escape", "back", "Back"),
                ("enter, ctrl+j, ctrl+m", "open_option", "Open", )]

    def on_key(self, event: Key):
        """Pass"""
        if event.key == "enter":
            self.action_open_option()

    def compose(self) -> ComposeResult:
        yield Header()
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

        self.app.switch_screen(SingleReference(self.references[self.option_id]))

    def action_back(self):
        """Closes screen, triggered by keystroke"""
        self.app.pop_screen()


class SingleReference(Screen[None]):
    """Screen containing a single reference."""
    CSS_PATH = "style.tcss"

    BINDINGS = [("d", "delete_reference", "Delete"),
                ("escape", "back", "Back")]

    def __init__(self, reference: Reference, start_selected_coord: Coordinate | None = None):
        super().__init__()
        self.reference = reference
        self.sub_title = f"{self.reference.reference_type.value}: {self.reference.key}"
        self.start_selected_coord = start_selected_coord

    def compose(self) -> ComposeResult:
        yield Header()
        yield SingleReferenceWidget(self.reference, self.start_selected_coord)
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

        def confirm(confirmation):
            if confirmation:
                try:
                    self.app.reference_services.delete_reference(self.reference.key)
                    self.app.notify(f"{self.reference.key} succesfully removed from DB")
                    self.app.pop_screen()
                except sqlite3.Error:
                    self.app.notify("Error, could not delete reference.")

        self.app.push_screen(ConfirmationScreen('delete this entry'), confirm)


class SingleLineTextArea(TextArea):
    """TextArea with new line disabled."""
    async def _on_key(self, event: events.Key):
        if event.key in ["enter", "ctrl+j"]:
            event.prevent_default()
            self.post_message(ModifyField())


class ModifyField(Message):
    """Message sent when hitting enter on modified field."""


class SingleReferenceWidget(Widget):
    """Widget for displaying a single reference."""
    # (row_index, key, value)
    modify_field: tuple | None = reactive(None)

    def __init__(self, reference: Reference, start_selected_coord: Coordinate | None = None):
        super().__init__(classes="single-ref")
        self.reference: Reference = reference
        self.start_selected_coord = start_selected_coord
        self.last_selected_coord = start_selected_coord

    def compose(self) -> ComposeResult:
        table = DataTable()
        table.add_column(self.reference.reference_type.value, width=15)
        table.add_column(self.reference.key)
        for field, value in self.reference.fields.items():
            if value is None:
                continue
            table.add_row(field, str(value))
        if self.start_selected_coord is not None:
            table.move_cursor(row=self.start_selected_coord.row,
                              column=self.start_selected_coord.column)
        yield table

        t = SingleLineTextArea(classes="modify-field")
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

    @on(ModifyField)
    def field_modified(self):
        """Catch message from modify field."""
        table = self.query_one(DataTable)
        if self.modify_field is not None:
            field = self.query_one(TextArea)
            try:
                self.app.reference_services.validate_field(self.modify_field[1], field.text)

                self.reference.fields[self.modify_field[1]] = field.text
                self.app.reference_repository.delete_from_db(self.reference.key)
                self.app.reference_repository.save(self.reference)


                self.app.switch_screen(SingleReference(self.reference, table.cursor_coordinate))
            except ValueError as error:
                self.notify(f"Error: {error}", severity="error")

    def on_key(self, event: events.Key):
        """Open modify field on enter. Close field on escape."""
        table = self.query_one(DataTable)
        if event.key in ["enter", "ctrl+j"] and table.cursor_coordinate.column == 1 \
                and self.modify_field is None:
            row = table.cursor_coordinate.row
            field, value = table.get_row_at(row)
            self.modify_field = (row, field, value)
        if event.key == "escape":
            self.modify_field = None
