from ui import UI
from entities.reference import Reference
from textual import events, on
from textual.app import App,  ComposeResult
from textual.widgets import Header, Footer, Button, Label, Static, OptionList
from textual.widgets.option_list import Option
from textual.containers import Grid, Center
from textual.screen import ModalScreen, Screen


class QuitScreen(ModalScreen):

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


class SingleReference(ModalScreen[None]):

    def __init__(self, references, reference_id) -> None:
        super().__init__()
        self.reference = references[reference_id]

    BINDINGS = [("escape", "app.pop_screen")]

    def compose(self) -> ComposeResult:
        yield Center(Label(str(self.reference)), id="dialog")


class ShowAll(Screen[None]):
    def __init__(self, references) -> None:
        super().__init__()
        self.references = [Label(str(ref)) for ref in references]

    BINDINGS = [("m", "back_to_menu", "Main Menu")]

    def compose(self) -> ComposeResult:
        yield Center(
            *self.references)

    def action_back_to_menu(self):
        self.app.pop_screen()


class ListKeys(Screen[None]):
    def __init__(self, references: list[Reference]) -> None:
        super().__init__()
        self.references = references
        self.option_items = [Button(ref.key, id=index)
                             for index, ref in enumerate(references)]
        self.option_id = 0

    BINDINGS = [("m", "back_to_menu", "Main Menu"),
                ("o", "open_option", "Open")]

    def compose(self) -> ComposeResult:
        yield Center(*self.option_items, id="optionList")

    def on_button_click(self, event: Button.Pressed):
        self.app.switch_screen(SingleReference(
            self.references, event.button.id))

    def action_open_option(self):
        self.app.switch_screen(SingleReference(
            self.references, self.option_id))

    def action_back_to_menu(self):
        self.app.pop_screen()


class GUI(App[None]):

    def __init__(self, ui: UI):
        super().__init__()
        self.ui = ui

    CSS_PATH = "css/modal.tcss"
    BINDINGS = [("q", "request_quit", "Quit"), ("s", "show_all", "Show All"),
                ("l", "list_references", "List Keys"), ("a",
                                                        "add_reference", "Add Reference"),
                ]

    def compose(self) -> ComposeResult:
        yield Header("References to Bibtex")
        yield Static("Welcome to your vault of references!")
        yield Grid(Button("Show all references in Bibtex", id="showInBib"), Button("List reference keys", id="listAll"), Button("Add Reference", id="addRef"), id="menuGrid")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "showInBib":
            self.action_show_all()
        elif event.button.id == "listAll":
            self.action_list_references()

    def action_show_all(self):
        references = self.ui.show_references()
        self.push_screen(ShowAll(references))

    def action_list_references(self):
        references = self.ui.show_references()
        self.push_screen(ListKeys(references))

    def action_request_quit(self):
        self.push_screen(QuitScreen())
