"""Module containing GUI screen to show all
the references, currently in BibTex form,
but will be modified to show more user friendly
output

    Yields:
        Screen: Textual Widget
    """
from textual import work
from textual.app import ComposeResult
from textual.widgets import Header, Footer
from textual.screen import Screen
from textual.containers import Center, VerticalScroll
from textual.widgets import RadioSet, RadioButton, Input, Markdown


class ShowAll(Screen[None]):
    """Screen that shows all references in
    BibTex style and allows user to filter references"""

    def __init__(self, references, ref_services) -> None:
        super().__init__(classes="showall")
        self.sub_title = "Show all references"
        self.references = references
        self.ref_services = ref_services
        self.border = True
        self.index = 0


    BINDINGS = [("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(id="input", placeholder="Filter")
        with Center():
            with RadioSet():
                yield RadioButton("Author", value= True)
                yield RadioButton("Year")
                yield RadioButton("Title")
        with VerticalScroll(id="results-container"):
            yield Center(Markdown(id="results"))
        yield Footer()


    def on_mount(self) -> None:
        """Called when app starts."""
        radioset = self.query_one(RadioSet)
        radioset.border_title = "Filter by:"
        radioset.border_subtitle = "Results:"
        markdown = self.make_data_string(self.references)
        self.query_one("#results", Markdown).update(markdown)


    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Takes care of radio index change"""
        self.index = event.radio_set.pressed_index
        search = self.query_one('#input', Input)
        self.lookup_references(search.value)


    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_references(message.value)
        else:
            markdown = self.make_data_string(self.references)
            self.query_one("#results", Markdown).update(markdown)


    @work(exclusive=True)
    async def lookup_references(self, word: str) -> None:
        """Gets user input and calls for new reference list

        Args:
            word (str): user input
        """
        temp_ref = self.ref_services.filter_references(self.references, self.index, word)
        markdown =  self.make_data_string(temp_ref)
        self.query_one("#results", Markdown).update(markdown)


    def make_data_string(self, temp_ref: list):
        """Constructs a string of references

        Args:
            temp_ref (list): list filtered based on user input

        Returns:
            String: Markdown string
        """
        lines = []
        if isinstance(temp_ref, list):
            for ref in temp_ref:
                lines.append(f"# *{ref.reference_type.value}*: **{ref.key}**")
                for field, value in ref.fields.items():
                    if value is None:
                        continue
                    lines.append(f"###### {field.capitalize():25}{str(value)}")
        return "\n".join(lines)


    def action_back(self):
        """Closes the screen and goes back to previous
        triggered by keystroke"""
        self.app.pop_screen()
