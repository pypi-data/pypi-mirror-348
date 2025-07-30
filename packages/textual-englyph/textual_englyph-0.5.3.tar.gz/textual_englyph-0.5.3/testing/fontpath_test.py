"""Boilerplate code for testing purposes"""

from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText


class Test(App):
    """Test console markup styling the englyph text use case"""

    def compose(self) -> ComposeResult:
        yield EnGlyphText("Hello [red]Textual!", font_name="/tmp/BirchLeaf.ttf", font_size=32)


if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
