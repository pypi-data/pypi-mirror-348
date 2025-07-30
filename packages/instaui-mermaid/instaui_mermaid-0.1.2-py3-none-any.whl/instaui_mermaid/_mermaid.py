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
    """
    A UI component to render Mermaid diagrams from text-based syntax.

    Args:
        graph (ui.TMaybeRef[str]): A string containing the Mermaid diagram definition. 
                     This defines the structure and appearance of the diagram using Mermaid's syntax.
    
    Example:
    .. code-block:: python
        from instaui import ui

        @ui.page()
        def home():
            graph = '''
            graph TB
            FullFirstSquad-->StripedFirstSquad
            '''
            ui.mermaid(graph)
    """    

    def __init__(self, graph: ui.TMaybeRef[str]):    
        super().__init__()
        self.props({"graph": graph})
