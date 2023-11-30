"""Module constisting of all the GUI-screens
    that are shown to user.

    Yields:
        Screen: Textual Screen Widgets
    """

from textual.binding import Binding
from textual.app import App,  ComposeResult
# from textual.events import Key
from textual.widgets import Header, Footer, Button, Input, RichLog
from textual.containers import Center
from textual.screen import Screen
from screens.confirmation_screen import ConfirmationScreen
from screens.add_reference import AddReference
from screens.list_keys import ListKeys
from screens.show_all import ShowAll
from services.reference_services import ReferenceServices
from repositories.reference_repository import ReferenceRepository


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


class GUI(App[None]):
    """Main app that shows menu screen and buttons
    to open wanted subscreen"""

    def __init__(self, reference_repository: ReferenceRepository,
                 reference_services: ReferenceServices):
        super().__init__()
        self._reference_repository = reference_repository
        self._reference_services = reference_services
        self.references = self._reference_repository.load_all()
        self.show_all = Button("Show in BibTex format", id="toBibtex")
        self.list_keys = Button(
            "List all references", id="listAll")
        self.add_new = Button("Add new", id="addNew")

    CSS_PATH = "screens/style.tcss"

    BINDINGS = [("q", "request_quit", "Quit"), ("s", "show_all", "Show file"),
                ("l", "list_references", "List view"), ("a", "add_reference", "Add"),
                Binding("t", "test_screen", "test", show=False)
                ]
    INITIAL_VALUE = 1

    def compose(self) -> ComposeResult:
        yield Header(name="Vault of references")
        yield Center(self.show_all, self.list_keys, self.add_new)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        """Tracks button press events and
        calls for approriate method

        Args:
            event (Button.Pressed): Textual event message
        """
        if event.button.id == "toBibtex":
            self.action_show_all()
        elif event.button.id == "listAll":
            self.action_list_references()
        elif event.button.id == "addNew":
            self.action_add_reference()

    # Korjataan tää käyttöön seuraavassa sprintissä
    # def on_key(self, key: Key):
    #     """Tracks if Enter button presses happen on focused
    #     button"""
    #     if key.key in ["enter", "ctrl+j"]:
    #         key.stop()
    #         if self.show_all.has_focus:

    #             self.action_show_all()
    #         elif self.list_keys.has_focus:
    #             self.action_list_references()
    #         elif self.add_new.has_focus:
    #             self.action_add_reference()

    def action_show_all(self):
        """Opens screen that shows all references
        in BibTex format
        """
        self.push_screen(ShowAll(self.references))

    def action_list_references(self):
        """Opens screen that shows all reference
        keys as optionlist"""
        self.push_screen(ListKeys(self.references, self._reference_services.delete_reference,
                         self._reference_services.create_reference))

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
        def confirm_quit(quit_app: bool):
            if quit_app:
                self.exit()

        self.push_screen(ConfirmationScreen("quit"), confirm_quit)
