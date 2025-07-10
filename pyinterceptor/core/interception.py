import ctypes
import ctypes.wintypes as wintypes
import logging
from dataclasses import dataclass
from typing import Callable

from pyinterceptor.core import Device, InputStateManager
from pyinterceptor.defs import FilterKeyState, FilterMouseState, KeyState, KeyStroke, MouseStroke, Key
from pyinterceptor.exceptions import DeviceNotFoundError, DriverLoadError, DeviceIoError
from pyinterceptor.utils import decorators

# Win32 API for waiting on multiple handles
WaitForMultipleObjects = ctypes.windll.kernel32.WaitForMultipleObjects
WaitForMultipleObjects.restype = wintypes.DWORD

# Constants for wait results and limits
WAIT_TIMEOUT = 0x102
WAIT_OBJECT_0 = 0x0
INFINITE = 0xFFFFFFFF
MAX_DEVICES = 20

CallbackType = Callable[[Device, KeyStroke | MouseStroke, set[Key]], None]


@dataclass
class InputEventResult:
    """Represents the result of an input event received from a device.

    Attributes:
        device_path (str): The device path string.
        stroke (KeyStroke): The input stroke (keyboard or mouse).
        is_suppress (bool): Whether the input was suppressed by a listener.
    """
    device_path: str
    stroke: KeyStroke
    is_suppress: bool


@decorators.singleton
class Interception:
    """Main driver class that manages multiple interception devices and input event dispatching."""

    def __init__(self):
        self.devices: list[Device] = []
        self._handles = None
        self._listeners: list[Callable[[Device, KeyStroke | MouseStroke], bool]] = []

        self.input_state_manager = InputStateManager()

        self._open_all_devices()
        self._prepare_handle_array()

    def _open_all_devices(self):
        """Attempts to open all interception devices up to MAX_DEVICES.

        Devices that fail to open are skipped silently.

        Raises:
            RuntimeError: If no devices could be opened.
        """
        for i in range(MAX_DEVICES):
            device_path = fr"\\.\interception{str(i).zfill(2)}"
            try:
                device = Device(device_path)

                if (hwid := device.get_hwid()) is not None:
                    self.devices.append(device)
                    logging.debug(f"Opened {device_path}(hwid: {hwid})")
            except (DeviceNotFoundError, DeviceIoError):
                # Device path not available or failed to open; ignore
                continue

        if not self.devices:
            raise DriverLoadError("No interception devices could be opened.")

    def _prepare_handle_array(self):
        """Prepares an array of event handles from opened devices for waiting."""
        handle_array_type = wintypes.HANDLE * len(self.devices)
        self._handles = handle_array_type(*(d.event for d in self.devices))

    @staticmethod
    def _is_keyboard(device):
        """Determines if a device is a keyboard based on its device path index.

        Args:
            device (Device): The device to check.

        Returns:
            bool: True if device is a keyboard.
        """
        idx = int(device.device_path[-2:])
        return 1 <= idx <= 10

    @staticmethod
    def _is_mouse(device):
        """Determines if a device is a mouse based on its device path index.

        Args:
            device (Device): The device to check.

        Returns:
            bool: True if device is a mouse.
        """
        idx = int(device.device_path[-2:])
        return 11 <= idx <= 20

    def set_filter_keyboard(self, filter_key_state: FilterKeyState = FilterKeyState.ALL):
        """Applies a keyboard filter to all keyboard devices.

        Args:
            filter_key_state (FilterKeyState): The filter mask to apply.
        """
        for device in self.devices:
            if device.is_keyboard:
                device.set_filter(filter_key_state)

    def set_filter_mouse(self, filter_mouse_state: FilterMouseState = FilterMouseState.ALL):
        """Applies a mouse filter to all mouse devices.

        Args:
            filter_mouse_state (FilterMouseState): The filter mask to apply.
        """
        for device in self.devices:
            if device.is_mouse:
                device.set_filter(filter_mouse_state)

    def send(self, device: int | Device, stroke: KeyStroke | MouseStroke):
        """Sends an input stroke to a specified device.

        Args:
            device (int | Device): Device index or device instance.
            stroke (KeyStroke | MouseStroke): The input stroke to send.
        """
        if isinstance(device, int):
            device = self.devices[device]
        return device.send(stroke)

    def receive(self, timeout_ms: int = INFINITE) -> InputEventResult | None:
        """Waits for and receives an input event from any device within the timeout period.

        Args:
            timeout_ms (int): Timeout in milliseconds (default is infinite).

        Returns:
            InputEventResult | None: Result containing device path, stroke, and suppression flag, or None on timeout.
        """
        count = len(self.devices)
        index = WaitForMultipleObjects(count, self._handles, 0, timeout_ms)

        # Check if the wait result is within valid device indices
        if index < WAIT_OBJECT_0 or index >= WAIT_OBJECT_0 + count:
            return None

        device = self.devices[index - WAIT_OBJECT_0]
        stroke = device.receive()
        if stroke is None:
            return None

        # Update hardware key state
        self.input_state_manager.update_key_state(stroke=stroke, is_hardware=True)

        is_suppress = False
        # Call registered listeners; any listener returning True suppresses input
        for listener in self._listeners:
            is_suppress |= listener(device, stroke)

        is_key_down = not stroke.flags & KeyState.UP
        is_key_pressed = self.input_state_manager.is_pressed(stroke.code, False)

        # If not suppressed and key is down or already pressed by software, resend input and update software state
        if not is_suppress and (is_key_down or is_key_pressed):
            self.input_state_manager.update_key_state(stroke=stroke, is_hardware=False)
            device.send(stroke)

        return InputEventResult(device.device_path, stroke, is_suppress)

    def close(self):
        """Closes all opened devices and clears the device list."""
        for device in self.devices:
            device.close()
        self.devices.clear()

    def add_event_listener(self, callback: Callable[[Device, KeyStroke | MouseStroke], bool]):
        """Registers a callback listener that receives input strokes.

        Args:
            callback (Callable[[Device, KeyStroke | MouseStroke], bool]):
                A function that takes a stroke and returns True to suppress the input.
        """
        self._listeners.append(callback)
