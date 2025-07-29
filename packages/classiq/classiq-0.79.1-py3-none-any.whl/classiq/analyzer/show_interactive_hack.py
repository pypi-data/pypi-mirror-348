import os
import webbrowser
from typing import Callable, Union
from urllib.parse import urljoin

from classiq.interface.exceptions import ClassiqAnalyzerVisualizationError
from classiq.interface.generator.model.preferences.preferences import QuantumFormat
from classiq.interface.generator.quantum_program import QuantumProgram

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import is_notebook, syncify_function
from classiq.analyzer.url_utils import circuit_page_uri, client_ide_base_url
from classiq.visualization import (
    SerializedVisualModel,
    visualize_async,
)

VisualizationRenderer = Callable[[SerializedVisualModel, str], None]


def is_classiq_studio() -> bool:
    # Perhaps in the future we should add a dedicated unique environment var
    #  but so far should work just fine.
    return bool(os.environ.get("OPENVSCODE"))


def get_visualization_renderer() -> Union[VisualizationRenderer, None]:
    # Skip non-interactive environments
    if not is_notebook():
        return None
    # Ideally, we should check if a notebook renderer is available to handle custom
    #  mime type, or at least if the Classiq vscode extension is installed.
    #  There's no such capabilities in IPython, so we make assumption from a fact that
    #  it's a Classiq Studio env.
    #  (Studio always has the extension, and the extension always supports mime type).
    if not is_classiq_studio():
        return None
    try:
        # Must be available since is_notebook passed
        from IPython.display import display  # type: ignore[import]
    except ImportError:
        # Just in case it failed anyway, fallback to IDE link open
        return None

    def renderer(visual_model: SerializedVisualModel, fallback: str) -> None:
        display(
            {
                # Attempt to handle by notebook renderer from Classiq vscode extension
                "application/vnd.classiq+qviz": visual_model,
                # Fallback to IDE link display when no extension available.
                #  Shouldn't normally happen.
                #  Otherwise, is_classiq_studio detection is not correct.
                "text/plain": fallback,
            },
            raw=True,
        )

    return renderer


async def handle_remote_app(circuit: QuantumProgram, display_url: bool = True) -> None:
    if circuit.outputs.get(QuantumFormat.QASM) is None:
        raise ClassiqAnalyzerVisualizationError(
            "Missing QASM transpilation: visualization is only supported "
            "for QASM programs. Try adding QASM to the output formats "
            "synthesis preferences"
        )
    circuit_dataid = await ApiWrapper.call_analyzer_app(circuit)
    app_url = urljoin(
        client_ide_base_url(),
        circuit_page_uri(circuit_id=circuit_dataid.id, circuit_version=circuit.version),
    )
    link_label = f"Quantum program link: {app_url}"

    renderer = get_visualization_renderer()
    if renderer:
        # Visualize in-place
        visual_model = await visualize_async(circuit_dataid)
        renderer(visual_model, link_label)
        return

    if display_url:
        print(link_label)  # noqa: T201

    webbrowser.open_new_tab(app_url)


async def _show_interactive(self: QuantumProgram, display_url: bool = True) -> None:
    """
    Displays the interactive representation of the quantum program in the Classiq IDE.

    Args:
        self:
            The serialized quantum program to be displayed.
        display_url:
            Whether to print the url

    Links:
        [Visualization tool](https://docs.classiq.io/latest/reference-manual/analyzer/quantum-program-visualization-tool/)
    """
    await handle_remote_app(self, display_url)


QuantumProgram.show = syncify_function(_show_interactive)  # type: ignore[attr-defined]
QuantumProgram.show_async = _show_interactive  # type: ignore[attr-defined]
