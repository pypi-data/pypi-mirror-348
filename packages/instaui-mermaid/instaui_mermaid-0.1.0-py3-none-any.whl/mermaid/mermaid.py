from pathlib import Path
from instaui import ui

_STATIC_DIR = Path(__file__).parent / "static"
_MERMAID_JS_FILE = _STATIC_DIR / "mermaid.esm.min.mjs"


_IMPORT_MAPS = {"mermaid": _MERMAID_JS_FILE}


class Mermaid(
    ui.element,
    esm="./instaui-mermaid.js",
    externals=_IMPORT_MAPS,
):
    def __init__(self, graph: ui.TMaybeRef[str]):
        super().__init__()
        self.props({"graph": graph})
