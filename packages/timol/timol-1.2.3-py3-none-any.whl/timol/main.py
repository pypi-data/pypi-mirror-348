from typing import Iterable, List, Optional, Union

from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.containers import Horizontal
from textual.events import MouseEvent
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.validation import Number, Validator
from textual.widget import Widget
from textual.widgets import Header, Input

from timol.reader import MoleculesReader
from timol.sidebar import Sidebar
from timol.utils import Benchmarker
from timol.viewer import MolViewer


class InputScreen(ModalScreen):
    def __init__(
        self,
        placeholder: str = "",
        input_type: str = "text",
        validators: Optional[List[Validator]] = [],
    ):
        super().__init__()
        self.placeholder = placeholder
        self.input_type = input_type
        self.validators = validators

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder=self.placeholder,
            type=self.input_type,  # type: ignore
            validators=self.validators,
        )

    def on_key(self, event):
        if event.key == "escape":
            self.dismiss(None)

    def on_click(self, event: MouseEvent):
        if event.widget is self:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted):
        val = event.validation_result
        if val is not None and len(val.failures) > 0:
            if len(val.failure_descriptions) > 0:
                s = val.failure_descriptions[0]
            else:
                s = "Failed to validate"

            input = self.query_one(Input)
            input.placeholder = s
            input.clear()
            return

        self.dismiss(event.value)


class MoleculesInterface(Widget):
    index: reactive[int] = reactive(-1)
    centering: reactive[bool] = reactive(False)
    radii_scale: reactive[float] = reactive(1)
    bond_factor: reactive[float] = reactive(0.7)
    mode: reactive[str] = reactive("spheres")

    _modes: List[str] = ["spheres", "lines", "spheres&lines"]
    bmarker: Optional[Benchmarker] = None

    BINDINGS = [
        Binding("h", "toggle_hotkey_menu", "Toggle help menu"),
        Binding("a", "rotate_camera(-45,0,0)", "Rotate left"),
        Binding("d", "rotate_camera(45,0,0)", "Rotate right"),
        Binding("s", "rotate_camera(0,-45,0)", "Tilt backwards"),
        Binding("w", "rotate_camera(0,45,0)", "Tilt forwards"),
        Binding("z", "rotate_camera(0,0,45)", "Spin left"),
        Binding("x", "rotate_camera(0,0,-45)", "Spin right"),
        Binding("A", "pan_camera(-1,0)", "Pan left"),
        Binding("D", "pan_camera(1,0)", "Pan right"),
        Binding("S", "pan_camera(0, 1)", "Pan backwards"),
        Binding("W", "pan_camera(0,-1)", "Pan forwards"),
        Binding("m", "change_mode()", "Change mode"),
        Binding("left, Q", "change_index(-1)", "Next frame (index)"),
        Binding("right, E", "change_index(1)", "Previous frame (index)"),
        Binding("up", "set_index(-1)", "Last frame (index = -1)"),
        Binding("down", "set_index(0)", "First frame (index = 0)"),
        Binding("e", "zoom(1)", "Zoom inwards"),
        Binding("q", "zoom(-1)", "Zoom outwards"),
        Binding("r", "reset_view()", "Reset camera rotation, zoom and offset"),
        Binding("R", "radii_scale_prompt", "Change the scale of the atomic radii"),
        Binding("B", "bond_factor_prompt", "Change the factor for detecting bonds"),
        Binding("c", "toggle_centering()", "Center camera"),
        Binding("i", "index_prompt", "Go to specific frame (index)"),
        Binding("b", "toggle_sidebar", "Toggle sidebar visibility"),
    ]

    def __init__(
        self,
        mols_reader: MoleculesReader,
        radii_scale: float = 1,
        bmarker: Optional[Benchmarker] = None,
    ):
        super().__init__()
        self.mols_reader = mols_reader
        self.radii_scale = radii_scale
        self.bmarker = bmarker
        self.load_molecules()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield (
                Sidebar(mols_reader=self.mols_reader)
                .data_bind(index=MoleculesInterface.index)
                .data_bind(centering=MoleculesInterface.centering)
                .data_bind(mode=MoleculesInterface.mode)
            )
            yield (
                MolViewer(mols_reader=self.mols_reader, bmarker=self.bmarker)
                .data_bind(index=MoleculesInterface.index)
                .data_bind(centering=MoleculesInterface.centering)
                .data_bind(radii_scale=MoleculesInterface.radii_scale)
                .data_bind(bond_factor=MoleculesInterface.bond_factor)
                .data_bind(mode=MoleculesInterface.mode)
            )

    def load_molecules(self) -> None:
        self.index = 0

    def set_index(self, index: Union[None, str, int] = None):
        n_mols = self.mols_reader.get_n_molecules()
        if index is None:
            return
        index = int(index)
        if index < 0:
            return self.set_index(index % n_mols)
        if index >= n_mols or index == self.index:
            return

        self.index = index

    def set_radii_scale(self, scale: Union[None, str, float] = None):
        if scale is None:
            return
        scale = float(scale)
        if scale <= 0:
            return
        self.radii_scale = scale

    def set_bond_factor(self, bond_factor: Union[None, str, float] = None):
        if bond_factor is None:
            return
        bond_factor = float(bond_factor)
        if bond_factor <= 0:
            return
        self.bond_factor = bond_factor

    def action_change_index(self, by: int):
        index = self.index + by
        if index < 0:
            return
        if index >= self.mols_reader.get_n_molecules():
            return
        self.set_index(self.index + by)

    def action_set_index(self, index: int):
        self.set_index(index)

    def action_reset_view(self):
        viewer = self.query_one(MolViewer)
        viewer.clear_rotation()
        viewer.scale = 10
        viewer.offset[:] = 0
        self.radii_scale = 1
        self.bond_factor = 0.7
        self.mode = "spheres"
        viewer.refresh()

    def action_toggle_centering(self):
        self.centering = not self.centering

    def action_zoom(self, by: int):
        self.query_one(MolViewer).zoom_by(by)

    def action_change_mode(self):
        current_index = self._modes.index(self.mode)
        new_mode = self._modes[(current_index + 1) % len(self._modes)]
        self.mode = new_mode
        self.query_one(MolViewer).refresh()

    def action_index_prompt(self):
        self.app.push_screen(
            screen=InputScreen(
                placeholder="Enter the index of the frame to jump to",
                input_type="integer",
                validators=[
                    Number(minimum=0, maximum=self.mols_reader.get_n_molecules() - 1)
                ],
            ),
            callback=self.set_index,  # type: ignore
        )

    def action_radii_scale_prompt(self):
        self.app.push_screen(
            screen=InputScreen(
                placeholder=f"Enter the scale of the atomic radii (currently {self.radii_scale})",
                input_type="number",
                validators=[Number(minimum=0)],
            ),
            callback=self.set_radii_scale,  # type: ignore
        )

    def action_bond_factor_prompt(self):
        self.app.push_screen(
            screen=InputScreen(
                placeholder=f"Enter the factor to consider bonds (currently {self.bond_factor})",
                input_type="number",
                validators=[Number(minimum=0)],
            ),
            callback=self.set_bond_factor,
        )

    def action_toggle_hotkey_menu(self):
        if self.screen.query("HelpPanel"):
            self.app.action_hide_help_panel()
        else:
            self.app.action_show_help_panel()

    def action_rotate_camera(
        self, x_rotation: float, y_rotation: float, z_rotation: float
    ):
        self.query_one(MolViewer).rotate_camera(x_rotation, y_rotation, z_rotation)

    def action_pan_camera(self, x: float, y: float):
        self.query_one(MolViewer).shift_offset(x, y)

    def action_toggle_sidebar(self):
        sidebar = self.query_one(Sidebar)
        width = sidebar.styles.width
        if width is None or width.value == 0:
            sidebar.styles.width = 30
        else:
            sidebar.styles.width = 0


class Timol(App[str]):
    CSS_PATH = "timol.tcss"
    TITLE = "TIMOL"
    SUB_TITLE = "Terminal Interface MOLecular viewer"
    BINDINGS = [
        Binding("ctrl+q,ctrl+c", "quit", "Quit", priority=True),
    ]

    bmarker: Optional[Benchmarker] = None

    def __init__(
        self, mols_reader: MoleculesReader, radii_scale: float = 1, bmark: bool = False
    ):
        self.mols_reader = mols_reader
        self.radii_scale = radii_scale
        if bmark:
            self.bmarker = Benchmarker()

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield MoleculesInterface(
            self.mols_reader, radii_scale=self.radii_scale, bmarker=self.bmarker
        )

    def interface_toggle_sidebar(self):
        self.query_one(MoleculesInterface).action_toggle_sidebar()

    def interface_reset(self):
        self.query_one(MoleculesInterface).action_reset_view()

    def interface_set_index(self):
        self.query_one(MoleculesInterface).action_index_prompt()

    def interface_change_atomic_radii(self):
        self.query_one(MoleculesInterface).action_radii_scale_prompt()

    def interface_change_bond_factor(self):
        self.query_one(MoleculesInterface).action_bond_factor_prompt()

    def interface_center(self):
        self.query_one(MoleculesInterface).action_toggle_centering()

    def interface_change_mode(self):
        self.query_one(MoleculesInterface).action_change_mode()

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand(
            "Sidebar Visibility (b)",
            "Toggle the sidebar visibility (on/off)",
            self.interface_toggle_sidebar,
        )
        yield SystemCommand(
            "Reset (r)",
            "Reset camera rotation, zoom, offset, radii and bond factors",
            self.interface_reset,
        )
        yield SystemCommand(
            "Go to frame/index (i)",
            "Go to a specific index/frame of the given trajectory",
            self.interface_set_index,
        )
        yield SystemCommand(
            "Atomic radii scale (shift-R)",
            "Change the scale of all atomic radii",
            self.interface_change_atomic_radii,
        )
        yield SystemCommand(
            "Bonds factor (shift-B)",
            "Change the bond factor: the larger the factor, the further away atoms can be bonded",
            self.interface_change_bond_factor,
        )
        yield SystemCommand(
            "Center molecule (c)",
            "Toggle whether the molecule should be centered (i.e. center of mass = 0)",
            self.interface_center,
        )

        modes = MoleculesInterface._modes
        modes_str = ", ".join(modes[:-1])
        modes_str += f" and {modes[-1]}"
        yield SystemCommand(
            "Change viewing mode (m)",
            f"Cycle the viewing mode between {modes_str}",
            self.interface_change_mode,
        )


if __name__ == "__main__":
    from timol.cli.main import cli

    cli()
