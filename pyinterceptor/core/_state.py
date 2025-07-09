from typing import Set

from ..types import Key, KeyStroke, MouseStroke
from ..utils.decorators import singleton


@singleton
class InputStateManager:
    """Manages the current state of pressed keys, distinguishing between hardware and software inputs.

    Attributes:
        pressed_hardware_keys (Set[Key]): Set of keys currently pressed by hardware input.
        pressed_software_keys (Set[Key]): Set of keys currently pressed by software input.
    """

    def __init__(self):
        self.pressed_hardware_keys: Set[Key] = set()
        self.pressed_software_keys: Set[Key] = set()

    def update_key_state(self, key: Key | int = None, is_down: bool = None, is_hardware: bool = None,
                         stroke: KeyStroke = None):
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
            # Extract key info from KeyStroke if parameters are not explicitly provided
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

    def is_pressed(self, key: Key, is_hardware: bool) -> bool:
        """Checks whether a specific key is currently pressed.

        Args:
            key (Key): The key to check.
            is_hardware (bool): True to check hardware keys, False for software keys.

        Returns:
            bool: True if the key is pressed, False otherwise.
        """
        target_set = self.pressed_hardware_keys if is_hardware else self.pressed_software_keys
        return key in target_set

    def get_all_pressed_keys(self) -> Set[Key]:
        """Returns the union of all currently pressed keys (hardware and software).

        Returns:
            Set[Key]: A set containing all pressed keys.
        """
        return self.pressed_hardware_keys.union(self.pressed_software_keys)
