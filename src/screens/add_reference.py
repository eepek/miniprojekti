"""Module containing GUI-screens related to adding
a reference

    Yields:
        Screen: Textual widget
    """

from textual import on
from textual.app import ComposeResult
from textual.events import Key
from textual.widgets import Header, Footer, Button, OptionList, Input, RichLog
from textual.widgets.option_list import Option
from textual.containers import Center
from textual.screen import Screen
from services.reference_services import ReferenceServices
from entities.reference import ReferenceType
from constants import TECHREPORT_KEYS, INPROCEEDINGS_KEYS


class AddReference(Screen):
    """Screen used to select the type of
    reference user wants to create
    """
    CSS = """
        OptionList {
            width: 50%;
            margin: 2;
}
      """
    BINDINGS = [("b", "back", "Back"),
                ("o, enter, ctrl+j", "open_option", "Open", )]

    def __init__(self, reference_services: ReferenceServices) -> None:
        super().__init__()
        self.option_id = ""
        self.services = reference_services

    def compose(self) -> ComposeResult:
        reference_types = [
            Option("TechReport", id="techreport"),
            Option("Inproceedings", id="inproceedings")
        ]
        yield Header()
        yield Center(OptionList(*reference_types, id="option_list"))
        yield Footer()

    @on(OptionList.OptionMessage)
    def user_selected(self, event: OptionList.OptionSelected):
        """Gets Id for current selection on the option list

        Args:
            event (OptionList.OptionSelected): Textual message
        """
        self.option_id = "techreport" if event.option_index == 0 else "inproceedings"

    def action_open_option(self):
        """Opens form for selected reference type
        """

        def save_reference(reference: dict) -> None:
            # self.query_one(RichLog).write(reference)
            # self.query_one(RichLog).write(self.option_id)
            ref_type = ReferenceType(self.option_id)
            self.services.create_reference(ref_type, reference)

        self.app.push_screen(ReferenceForm(
            self.option_id), save_reference)

    def action_back(self):
        """Closes the screen, triggered by key stroke"""
        self.app.pop_screen()


class ReferenceForm(Screen[dict]):
    """Screen that shows form for adding a new reference.
    Returns the reference"""

    CSS = """
        .input-field {
            width: 50%;
            height: 4;
        }
    """

    BINDINGS = [("h", "save", "Save"), ("ctrl+q", "cancel", "Cancel")]

    def __init__(self, reference_type: str) -> None:
        self.keys = TECHREPORT_KEYS if reference_type == "techreport" else INPROCEEDINGS_KEYS
        self.inputs = [Input(placeholder=field, id=field, classes="input-field")
                       for field in self.keys]
        super().__init__()
        self.new_reference = {}
        self.save_button = Button("Save", id="save")
        self.cancel_button = Button("Cancel", id="cancel")

    def compose(self):

        yield Center(*self.inputs)
        yield RichLog()
        yield Center(self.save_button, self.cancel_button)
        yield Footer()

    def on_input_changed(self, message: Input.Changed):
        """When value of one of the input fields is changed"""
        input_id = message.input.id
        self.new_reference.update({input_id: message.value})

    # Button actions

    def on_button_pressed(self, event: Button.Pressed):
        """Button press calls approiate function"""
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()

    def on_key(self, key: Key):
        """Tracks if Enter button presses happen on focused
        button"""
        if key.key in ["enter", "ctrl+j"]:
            if self.save_button.has_focus:
                self.action_save()
            elif self.cancel_button.has_focus:
                self.action_cancel()

    def action_cancel(self):
        """Closes the screen, triggered by key"""
        self.app.pop_screen()

    def action_save(self):
        """Returns the added reference from input fields as a
        Reference object"""
        self.dismiss(self.new_reference)
