from typing import Set, Union

from pyinterceptor import MouseButton, MouseState
from ..defs import Key, KeyStroke, MouseStroke
from ..utils.decorators import singleton


@singleton
class InputStateManager:
    """Manages the current state of pressed keys and mouse buttons,
    distinguishing between hardware and software input sources.

    This class tracks which keys and mouse buttons are currently pressed,
    separated into hardware-generated and software-generated events.

    Attributes:
        pressed_hardware_keys (Set[Key]): Keys currently pressed by hardware input.
        pressed_software_keys (Set[Key]): Keys currently pressed by software input.
        pressed_hardware_buttons (Set[MouseButton]): Mouse buttons pressed by hardware input.
        pressed_software_buttons (Set[MouseButton]): Mouse buttons pressed by software input.
    """

    def __init__(self):
        self.pressed_hardware_keys: Set[Key] = set()
        self.pressed_software_keys: Set[Key] = set()
        self.pressed_hardware_buttons: Set[MouseButton] = set()
        self.pressed_software_buttons: Set[MouseButton] = set()

    def update_key_state(
            self,
            key: Key | int = None,
            is_down: bool = None,
            is_hardware: bool = None,
            stroke: KeyStroke = None
    ):
        """Updates the key state by adding or removing keys from pressed sets.

        This method accepts either individual parameters or a KeyStroke object
        to update the pressed key sets accordingly.

        Args:
            key (Key | int, optional): The key code or Key enum to update.
            is_down (bool, optional): True if key is pressed down, False if released.
            is_hardware (bool, optional): True if the event is from hardware, False if software.
            stroke (KeyStroke, optional): A KeyStroke object containing key info.

        Raises:
            ValueError: If neither a complete set of parameters nor a stroke is provided.
        """
        if stroke:
            if key is None:
                key = stroke.code
            if is_down is None:
                is_down = stroke.is_down
            if is_hardware is None:
                is_hardware = stroke.is_hardware

        if key is None or is_down is None or is_hardware is None:
            raise ValueError("Either provide stroke or explicitly specify key, is_down, and is_hardware.")

        # Normalize key to Key enum if an int is given
        if not isinstance(key, Key):
            key = Key(key)

        # Select target set based on input source (hardware/software)
        target_set = self.pressed_hardware_keys if is_hardware else self.pressed_software_keys
        if is_down:
            target_set.add(key)
        else:
            target_set.discard(key)

    def update_mouse_state(
            self,
            button: MouseButton | MouseState | int | None = None,
            is_down: bool | None = None,
            is_hardware: bool | None = None,
            stroke: MouseStroke | None = None
    ):
        """Updates the mouse button state based on event.

        Args:
            button (MouseButton | MouseState | int, optional): The button to update.
            is_down (bool, optional): True if button is pressed down.
            is_hardware (bool, optional): True if input is from hardware.
            stroke (MouseStroke, optional): Optional stroke from which to infer state.

        Raises:
            ValueError: If required arguments are missing.
        """
        if stroke:
            if button is None:
                button = MouseButton(stroke.button_flags)
            if is_down is None:
                is_down = stroke.button_flags in {button.down for button in MouseButton}
            if is_hardware is None:
                is_hardware = stroke.is_hardware

        if button is None or is_down is None or is_hardware is None:
            raise ValueError("Either provide stroke or explicitly specify button, is_down, and is_hardware.")

        # Normalize button to MouseButton
        if not isinstance(button, MouseButton):
            button = MouseButton(button)

        # Select target set based on input source (hardware/software)
        target_set = self.pressed_hardware_buttons if is_hardware else self.pressed_software_buttons
        if is_down:
            target_set.add(button)
        else:
            target_set.discard(button)

    def is_pressed(self, code: Key | MouseButton, is_hardware: bool) -> bool:
        """Checks whether a key or mouse button is currently pressed.

        Args:
            code (Key | MouseButton): The input code to check.
            is_hardware (bool): True to check hardware inputs, False for software.

        Returns:
            bool: True if the code is pressed.
        """
        if isinstance(code, Key):
            target_set = self.pressed_hardware_keys if is_hardware else self.pressed_software_keys
        elif isinstance(code, MouseButton):
            target_set = self.pressed_hardware_buttons if is_hardware else self.pressed_software_buttons
        else:
            raise TypeError("Input must be of type Key or MouseButton.")

        return code in target_set

    def get_all_pressed_keys(self) -> Set[Key]:
        """Returns all currently pressed keyboard keys (hardware and software).

        Returns:
            Set[Key]: A set of pressed keyboard keys.
        """
        return self.pressed_hardware_keys | self.pressed_software_keys

    def get_all_pressed_buttons(self) -> Set[MouseButton]:
        """Returns all currently pressed mouse buttons (hardware and software).

        Returns:
            Set[MouseButton]: A set of pressed mouse buttons.
        """
        return self.pressed_hardware_buttons | self.pressed_software_buttons

    def get_all_pressed_inputs(self) -> Set[Union[Key, MouseButton]]:
        """Returns all currently pressed keys and mouse buttons.

        Returns:
            Set[Union[Key, MouseButton]]: A set of all pressed inputs.
        """
        return self.get_all_pressed_keys() | self.get_all_pressed_buttons()
