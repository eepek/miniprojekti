from textual import events
from ui import UI
from entities.reference import Reference
from components.reference_item import ReferenceItem
from textual.app import App,  ComposeResult
from textual.widgets import Header, Footer, Button, Label, Static, OptionList
from textual.widgets.option_list import Option
from textual.containers import Grid, Center
from textual.screen import ModalScreen, Screen


class QuitScreen(Screen):

    BINDINGS = [("q", "exit", "Quit"),
                ("c", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Do you want to exit the application?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()

    def action_exit(self):
        self.app.exit()

    def action_cancel(self):
        self.app.pop_screen()


class SingleReference(Screen[None]):

    def __init__(self, references, reference_id) -> None:
        super().__init__()
        self.reference = references[reference_id]

    BINDINGS = [("e", "edit_reference", "Edit"),
                ("d", "delete_reference", "Delete")]

    def compose(self) -> ComposeResult:
        yield Center(Label(str(self.reference)), id="dialog")


class ListKeys(Screen[None]):
    def __init__(self, references: list[Reference]) -> None:
        super().__init__()
        self.references = references
        self.option_items = [Option(ref.key, id=ref.key)
                             for ref in references]
        self.option_id = 0

    BINDINGS = [("b", "back_to_menu", "Back"),
                ("o", "open_option", "Open")]

    def compose(self) -> ComposeResult:
        yield Center(OptionList(*self.option_items, id="optionList"))

    @on(OptionList.OptionMessage)
    def user_selected(self, event: OptionList.OptionSelected):
        self.option_id = event.option_index

    def action_open_option(self):
        self.app.switch_screen(SingleReference(
            self.references, self.option_id))

    def action_back_to_menu(self):
        self.app.pop_screen()


class ShowAll(Screen[None]):
    def __init__(self, references) -> None:
        super().__init__()
        self.references = references

    def compose(self) -> ComposeResult:
        self.textfile = Static(*str(self.references))
        yield self.textfile

    def on_mount(self) -> None:
        self.textfile.styles.width = "50%"


class GUI(App[None]):

    def __init__(self, ui: UI):
        super().__init__()
        self.ui = ui
        self.references = self.ui.show_references()

    CSS_PATH = "css/modal.tcss"
    BINDINGS = [("q", "request_quit", "Quit"), ("s", "show_all", "Show file"),
                ("l", "list_references", "List view"), ("a",
                                                        "add_reference", "Add"),
                ]

    def compose(self) -> ComposeResult:
        Header(name="Vault of references")
        Center(Button("Show in BibTex format", id="toBibtex"), Button(
            "List all references", id="listAll"), Button("Add new", id="addNew"))
        Footer()

    def action_show_all(self):
        self.push_screen(ListKeys)

    def action_request_quit(self):
        self.push_screen(QuitScreen())
