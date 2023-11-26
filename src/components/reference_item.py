from entities.reference import Reference
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Label, Static, Switch


class ReferenceItem(Static):

    def __init__(self, reference: Reference) -> None:
        super().__init__()
        self._reference = reference

    DEFAULT_CSS = """
    ReferenceItem {
        background: $boost;
        border: heavy $panel-lighten-3;
        padding: 0 1;
    }

    .top-row {
        height: auto;
    }

    .top-row .referenceitem--collapsed {
        height: 3;
    }

    .referenceitem--show-more {
        width: auto;
    }

    .referenceitem--collapsed {
        display: none;
    }



    """

    def compose(self) -> ComposeResult:
        self._show_reference = Button(
            "View", classes="referenceitem--show-more")
        self._top_row = Horizontal(
            Label(self._reference.key), Label(self._reference.title),  self._show_reference, classes="top-row")
        self._content = Label(str(self._reference),
                              classes="referenceitem--collapsed")

        yield self._top_row
        yield self._content

    def on_button_pressed(self, event: Button.Pressed):
        event.stop()
        if self.is_collapsed:
            self.expand_reference()
        else:
            self.collapse_reference()

    def collapse_reference(self):
        self._content.add_class("referenceitem--collapsed")
        self._show_reference.label = "Hide"

    def expand_reference(self):
        self._content.remove_class("referenceitem--collapsed")
        self._show_reference.label = "View"

    @property
    def is_collapsed(self) -> bool:
        return self.has_class("referenceitem--collapsed")
