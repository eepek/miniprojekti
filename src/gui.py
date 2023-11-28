from textual import events, on
from ui import UI
from entities.reference import Reference
from textual.binding import Binding
from textual.app import App,  ComposeResult
from textual.widgets import Header, Footer, Button, Label, OptionList, Input, RichLog, Select
from textual.widgets.option_list import Option
from textual.containers import Grid, Center, Vertical
from textual.screen import ModalScreen, Screen


class QuitScreen(Screen):

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
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()

    # def on_button_selected(self, key: events.Key, message: Button.Selected):
    #     if key in ["ctrl+j", "enter", "newline"]:

    def action_exit(self):
        self.app.exit()

    def action_cancel(self):
        self.app.pop_screen()


class SingleReference(Screen[None]):

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
        self.app.pop_screen()


class TestScreen(Screen):

    def compose(self) -> ComposeResult:
        yield RichLog()
        yield Button("One", id="one")
        yield Button("Two", id="two")

    def on_key(self, event: Button._on_key) -> None:
        # self.query_one(RichLog).write(event)
        self.query_one(RichLog).write(event)
        Button.press(self)

    def on_button_pressed(self, event: Button.Pressed):
        self.query_one(RichLog).write(event.button.id)


class ListKeys(Screen[None]):
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
        self.option_id = event.option_index

    def action_open_option(self):
        self.app.switch_screen(SingleReference(
            self.references, self.option_id))

    def action_back(self):
        self.app.pop_screen()


class ShowAll(Screen[None]):
    def __init__(self, references) -> None:
        super().__init__()
        self.references = [Label(str(ref)) for ref in references]

    BINDINGS = [("b", "back", "Back")]

    def compose(self) -> ComposeResult:
        self.textfile = Center(*self.references)
        yield self.textfile
        yield Footer()

    def on_mount(self) -> None:
        self.textfile.styles.width = "50%"

    def action_back(self):
        self.app.pop_screen()


class AddReference(Screen):

    CSS = """
        OptionList {
            width: 50%;
            margin: 2;
}
      """
    BINDINGS = [("b", "back", "Back"),
                ("enter, ctrl+j", "open_option", "Open", )]

    def compose(self) -> ComposeResult:

        reference_types = [
            Option("TechReport", id="tech"),
            Option("Inproceedings", id="inpro")
        ]
        yield Header()
        yield Center(OptionList(*reference_types, id="option_list"))

    @on(OptionList.OptionMessage)
    def user_selected(self, event: OptionList.OptionSelected):
        self.option_id = event.option_index

    # def action_open_option(self):
    #     self.app.switch_screen(ReferenceForm(
    #         self.option_id))

    def action_back(self):
        self.app.pop_screen()

# class ReferenceForm(Screen[object]):


class GUI(App[None]):

    def __init__(self, ui: UI):
        super().__init__()
        self.ui = ui
        self.references = self.ui.show_references()

    CSS_PATH = "css/modal.tcss"
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

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)

    def action_show_all(self):
        self.push_screen(ShowAll(self.references))

    def action_list_references(self):
        self.push_screen(ListKeys(self.references))

    def action_add_reference(self):
        self.push_screen(AddReference())

    def action_test_screen(self):
        self.push_screen(TestScreen())

    def action_request_quit(self):
        self.push_screen(QuitScreen())
