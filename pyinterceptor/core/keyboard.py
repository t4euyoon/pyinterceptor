import random
import time
from typing import Sequence, Literal

from pyinterceptor.core import Interception, Device, InputStateManager
from pyinterceptor.defs import Key, KeyState, KeyStroke

# Type alias for delay mode
DelayMode = Literal["fixed", "humanic"]


class Keyboard:
    """Simulates keyboard input using the Interception driver.

    This class provides functionality to simulate key presses, releases,
    combinations, and sequences with either fixed or human-like delays.

    Attributes:
        device (Device | int): The target device to send input to.
    """

    def __init__(self, device: Device | int = 0):
        """Initializes the keyboard simulator.

        Args:
            device (Device | int): Device instance or device ID.
        """
        self.device = device

    def press(self, key: Key):
        """Sends a key down event.

        Args:
            key (Key): The key to press.

        Returns:
            bool: True if the event was sent successfully.
        """
        stroke = KeyStroke(key, KeyState.DOWN)
        return Interception().send(self.device, stroke)

    def release(self, key: Key):
        """Sends a key up event.

        Args:
            key (Key): The key to release.

        Returns:
            bool: True if the event was sent successfully.
        """
        stroke = KeyStroke(key, KeyState.UP)
        return Interception().send(self.device, stroke)

    def tap(self, key: Key, delay: int = 50, delay_mode: DelayMode = "fixed"):
        """Taps a key with optional delay mode.

        Args:
            key (Key): The key to tap.
            delay (int): Delay in milliseconds between press and release.
            delay_mode (DelayMode): 'fixed' or 'humanic' for delay behavior.

        Returns:
            bool: True if the press and release were successful.
        """
        press_result = self.press(key)
        if press_result:
            self._sleep(delay, delay_mode)
            return self.release(key)
        return False

    def type_keys(self, keys: Sequence[Key], delay: int = 50, delay_mode: DelayMode = "fixed"):
        """Types a sequence of keys.

        Args:
            keys (Sequence[Key]): List of keys to type.
            delay (int): Delay between each key tap in milliseconds.
            delay_mode (DelayMode): 'fixed' or 'humanic' for delay behavior.
        """
        for key in keys:
            self.tap(key, delay, delay_mode)

    def press_combo(self, keys: Sequence[Key], delay: int = 50, delay_mode: DelayMode = "fixed"):
        """Presses a combination of keys (e.g. Ctrl + Alt + Del).

        Presses all keys in order, then releases them in reverse order.

        Args:
            keys (Sequence[Key]): The key combination to press.
            delay (int): Delay between each key press/release in ms.
            delay_mode (DelayMode): 'fixed' or 'humanic' for delay behavior.
        """
        for key in keys:
            self.press(key)
            self._sleep(delay, delay_mode)

        for key in reversed(keys):
            self.release(key)
            self._sleep(delay, delay_mode)

    def is_pressed(self, key: Key, is_hardware: bool = True):
        """Checks whether a key is currently pressed.

        Args:
            key (Key): The key to check.
            is_hardware (bool): Whether to check hardware state only.

        Returns:
            bool: True if the key is currently pressed.
        """
        return InputStateManager().is_pressed(key, is_hardware)

    @staticmethod
    def _sleep(delay: int, delay_mode: DelayMode = "fixed"):
        """Sleeps for a given delay with optional human-like variation.

        Args:
            delay (int): Base delay time in milliseconds.
            delay_mode (DelayMode): 'fixed' or 'humanic' for ±10% variation.
        """
        if delay_mode == "humanic":
            # Add ±10% random variation to simulate skilled human typing
            variation = delay * 0.1
            delay = random.uniform(delay - variation, delay + variation)

        time.sleep(delay / 1000)
