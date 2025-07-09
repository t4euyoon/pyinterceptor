import time
from typing import Sequence

from . import Interception, Device, InputStateManager
from ..types import Key, KeyState, KeyStroke


class Keyboard:
    """Simulates keyboard input using Interception driver."""

    def __init__(self, device: Device | int = 0):
        self.device = device
        self.interception = Interception()
        self.input_state_manager = InputStateManager()
        # self.keyboard_id = driver.find_keyboard_device()  # You should implement this
        # self.mouse_id = driver.find_mouse_device()  # You should implement this

    def press(self, key: Key):
        """Presses a key."""
        stroke = KeyStroke(key, KeyState.DOWN)
        return self.interception.send(self.device, stroke)

    def release(self, key: Key):
        """Releases a key."""
        stroke = KeyStroke(key, KeyState.UP)
        return self.interception.send(self.device, stroke)

    def tap(self, key: Key, delay=50):
        """Taps a key with optional delay."""
        press_result = self.press(key)
        if press_result.success:
            self._sleep(delay)
            return self.release(key)

        return press_result

    def type_keys(self, keys: Sequence[Key], delay=50):
        """Types a sequence of keys."""
        for key in keys:
            self.tap(key, delay)

    def press_combo(self, keys: Sequence[Key], delay=50):
        """Presses a combination of keys (e.g. Ctrl + C)."""
        for key in keys:
            self.press(key)
            self._sleep(delay)

        for key in reversed(keys):
            self.release(key)
            self._sleep(delay)

    def is_pressed(self, key: Key, is_hardware: bool = True):
        """Checks if a key is pressed.

        Args:
            key (Key): Key to check.
            is_hardware (bool, optional): Whether to check hardware input. Defaults to True.

        Returns:
            bool: True if pressed, False otherwise.
        """
        return self.input_state_manager.is_pressed(key, is_hardware)

    # TODO: Move to utils
    @staticmethod
    def _sleep(delay: int):
        time.sleep(delay / 1000)


class Mouse:
    """Simulates mouse input using Interception driver."""

    def __init__(self, device: Device | int = 0):
        self.device = device
        self.interception = Interception()
        # self.keyboard_id = driver.find_keyboard_device()  # You should implement this
        # self.mouse_id = driver.find_mouse_device()  # You should implement this
    # def move_mouse(self, dx: int, dy: int):
    #     """Moves the mouse by a relative amount."""
    #     stroke = MouseStroke(dx=dx, dy=dy)
    #     interception.send(self.mouse_id, stroke)
    #
    # def click_mouse(self, button: MouseButton, delay: float = 0.05):
    #     """Clicks a mouse button."""
    #     self.mouse_button(button, MouseState.DOWN)
    #     time.sleep(delay)
    #     self.mouse_button(button, MouseState.UP)
    #
    # def mouse_button(self, button: MouseButton, state: MouseState):
    #     """Presses or releases a mouse button."""
    #     stroke = MouseStroke(button=button, state=state)
    #     interception.send(self.mouse_id, stroke)
    #
    # def scroll_wheel(self, vertical: int = 0, horizontal: int = 0):
    #     """Scrolls the mouse wheel."""
    #     stroke = MouseStroke(wheel_y=vertical, wheel_x=horizontal)
    #     interception.send(self.mouse_id, stroke)
