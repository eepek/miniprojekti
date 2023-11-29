"""Module constisting of all the GUI-screens
    that are shown to user.

    Yields:
        Screen: Textual Screen Widgets
    """

from textual import on
from textual.binding import Binding
from textual.app import App,  ComposeResult
from textual.widgets import Header, Footer, Button, Label, OptionList, Input, RichLog
from textual.widgets.option_list import Option
from textual.containers import Grid, Center
from textual.screen import Screen
from services.reference_services import ReferenceServices
from repositories.reference_repository import ReferenceRepository
from entities.reference import Reference, ReferenceType
from constants import TECHREPORT_KEYS, INPROCEEDINGS_KEYS


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
            self.app.exit()
        else:
            self.app.pop_screen()

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


class TestScreen(Screen):
    """Screen for general testing,
    logs key presses

    Args:
        Screen (_type_): _description_
    """

    def compose(self) -> ComposeResult:
        yield RichLog()
        yield Input(placeholder="", value="value", id="id")
        yield Button("One", id="one")
        yield Button("Two", id="two")

    # def on_key(self, event: Button._on_key) -> None:
    #     """Pass"""
    #     # self.query_one(RichLog).write(event)
    #     self.query_one(RichLog).write(event)
    #     Button.press(self)

    def on_input_changed(self, message: Input.Changed):
        """Test function"""
        input_info = message.input
        self.query_one(RichLog).write(input_info)

    def on_button_pressed(self, event: Button.Pressed):
        """

        Args:
            event (Button.Pressed): _description_
        """
        self.query_one(RichLog).write(event.button.id)


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
        yield RichLog()

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

    def compose(self):

        yield Center(*self.inputs)
        yield RichLog()
        yield Center(Button("Save", id="save"), Button("Cancel", id="cancel"))
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

    def action_cancel(self):
        """Closes the screen, triggered by key"""
        self.app.pop_screen()

    def action_save(self):
        """Returns the added reference from input fields as a
        Reference object"""
        self.dismiss(self.new_reference)


class GUI(App[None]):
    """Main app that shows menu screen and buttons
    to open wanted subscreen"""

    def __init__(self, reference_repository: ReferenceRepository,
                 reference_services: ReferenceServices):
        super().__init__()
        self._reference_repository = reference_repository
        self._reference_services = reference_services
        self.references = self._reference_repository.load_all()

    BINDINGS = [("q", "request_quit", "Quit"), ("s", "show_all", "Show file"),
                ("l", "list_references", "List view"), ("a", "add_reference", "Add"),
                Binding("t", "test_screen", "test", show=False)
                ]
    INITIAL_VALUE = 1

    def compose(self) -> ComposeResult:
        yield Header(name="Vault of references")
        yield Center(Button("Show in BibTex format", id="toBibtex"), Button(
            "List all references", id="listAll"), Button("Add new", id="addNew"))
        yield Footer()

    # @on(Select.Changed)
    # def select_changed(self, event: Select.Changed) -> None:
    #     self.title = str(event.value)

    def action_show_all(self):
        """Opens screen that shows all references
        in BibTex format
        """
        self.push_screen(ShowAll(self.references))

    def action_list_references(self):
        """Opens screen that shows all reference
        keys as optionlist"""
        self.push_screen(ListKeys(self.references))

    def action_add_reference(self):
        """Opens screen that shows optionlist for
        choosing reference type to add"""
        self.push_screen(AddReference(
            self._reference_services))

    def action_test_screen(self):
        """For testing"""
        self.push_screen(TestScreen())

    def action_request_quit(self):
        """Opens screen for quit dialog"""
        self.push_screen(QuitScreen())
