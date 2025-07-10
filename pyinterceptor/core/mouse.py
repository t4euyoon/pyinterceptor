import random
import time
from typing import Literal, Tuple

from pyinterceptor.core import Interception, Device, InputStateManager
from pyinterceptor.defs import MouseStroke, MouseState, MouseButton, MouseFlag

# Type alias for delay mode
DelayMode = Literal["fixed", "humanic"]


class Mouse:
    """Simulates mouse input using the Interception driver.

    This class supports sending mouse movement, clicks, drags,
    and scrolls with optional human-like timing behavior.

    Attributes:
        device (Device | int): Target mouse device or device ID.
    """

    def __init__(self, device: Device | int = 11):
        """Initializes the mouse simulator.

        Args:
            device (Device | int): Mouse device instance or index (default: 11).
        """
        self.device = device

    def move(self, dx: int = 0, dy: int = 0, *, absolute: bool = False):
        """
        Moves the mouse pointer.

        Args:
            dx (int): Horizontal movement or absolute X coordinate.
            dy (int): Vertical movement or absolute Y coordinate.
            absolute (bool): If True, use absolute coordinates; otherwise relative movement.

        Returns:
            bool: True if the move was successful.
        """
        flags = MouseFlag.MOVE_ABSOLUTE if absolute else MouseFlag.MOVE_RELATIVE
        stroke = MouseStroke(flags=flags, x=dx, y=dy)
        return Interception().send(self.device, stroke)

    def scroll(self, vertical: int = 0, horizontal: int = 0):
        """Scrolls the mouse wheel.

        Args:
            vertical (int): Vertical scroll amount.
            horizontal (int): Horizontal scroll amount.

        Returns:
            bool: True if the scroll was successful.
        """
        flags = MouseFlag.MOVE_RELATIVE
        if vertical != 0:
            flags |= MouseFlag.MOVE_RELATIVE  # movement flag still needed
            flags |= MouseFlag(0)  # no specific flag for vertical wheel in MouseFlag, rely on button_flags
        if horizontal != 0:
            flags |= MouseFlag.MOVE_RELATIVE

        # For wheel scrolls, button_flags holds the button event flags for wheel
        button_flags = MouseState.NONE
        button_data = 0
        if vertical != 0:
            button_flags |= MouseState.WHEEL
            button_data = vertical
        if horizontal != 0:
            button_flags |= MouseState.HWHEEL
            # MouseStroke 구조체에 horizontal wheel data 별도 필드 없으므로 button_data에 가중치 주기 어렵지만,
            # 휠은 보통 vertical or horizontal 중 하나씩 보내므로 분리 처리 필요할 수도 있음

        stroke = MouseStroke(flags=flags, button_flags=button_flags, button_data=button_data)
        return Interception().send(self.device, stroke)

    def click(self, button: MouseButton, delay: int = 50, delay_mode: DelayMode = "fixed"):
        """Performs a full mouse click (press + release).

        Args:
            button (MouseButton): The mouse button to click.
            delay (int): Delay between press and release in ms.
            delay_mode (DelayMode): 'fixed' or 'humanic'.

        Returns:
            bool: True if both press and release succeeded.
        """
        press_result = self._press(button)
        if press_result:
            self._sleep(delay, delay_mode)
            return self._release(button)
        return False

    def drag(self, button: MouseButton, path: Tuple[Tuple[int, int]], step_delay: int = 30,
             delay_mode: DelayMode = "fixed"):
        """Drags the mouse along a path while holding a button.

        Args:
            button (MouseButton): The mouse button to hold.
            path (Tuple[Tuple[int, int]]): Sequence of (dx, dy) steps.
            step_delay (int): Delay between each step.
            delay_mode (DelayMode): 'fixed' or 'humanic'.
        """
        if not self._press(button):
            return False

        for dx, dy in path:
            self.move(dx, dy)
            self._sleep(step_delay, delay_mode)

        return self._release(button)

    @staticmethod
    def is_pressed(button: MouseButton, is_hardware: bool = True) -> bool:
        """Checks whether a mouse button is currently pressed.

        Args:
            button (MouseButton): Button to check.
            is_hardware (bool): Whether to check hardware-only state.

        Returns:
            bool: True if the button is pressed.
        """
        return InputStateManager().is_pressed(button, is_hardware)

    def _press(self, button: MouseButton) -> bool:
        """Sends a button press event.

        Args:
            button (MouseButton): Button to press.

        Returns:
            bool: True if the event was sent.
        """
        stroke = MouseStroke(button_flags=button.down)
        return Interception().send(self.device, stroke)

    def _release(self, button: MouseButton) -> bool:
        """Sends a button release event.

        Args:
            button (MouseButton): Button to release.

        Returns:
            bool: True if the event was sent.
        """
        stroke = MouseStroke(button_flags=button.up)
        return Interception().send(self.device, stroke)

    @staticmethod
    def _sleep(delay: int, delay_mode: DelayMode = "fixed"):
        """Sleeps with optional human-like variation.

        Args:
            delay (int): Base delay in ms.
            delay_mode (DelayMode): 'fixed' or 'humanic'.
        """
        if delay_mode == "humanic":
            variation = delay * 0.1
            delay = random.uniform(delay - variation, delay + variation)
        time.sleep(delay / 1000)
