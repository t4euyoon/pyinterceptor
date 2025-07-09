import ctypes
import ctypes.wintypes as wintypes
from dataclasses import dataclass

from ._ioctl import IOCTL_READ, IOCTL_WRITE, IOCTL_SET_FILTER, IOCTL_SET_EVENT, IOCTL_GET_HARDWARE_ID
from ..types import FilterKeyState, FilterMouseState, KeyStroke, MouseStroke

# Win32 API function bindings
CreateFile = ctypes.windll.kernel32.CreateFileW
CreateEvent = ctypes.windll.kernel32.CreateEventW
CloseHandle = ctypes.windll.kernel32.CloseHandle
DeviceIoControl = ctypes.windll.kernel32.DeviceIoControl
WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject

# Define return types for clarity and safety
CreateFile.restype = wintypes.HANDLE
CreateEvent.restype = wintypes.HANDLE
CloseHandle.restype = wintypes.BOOL
DeviceIoControl.restype = wintypes.BOOL
WaitForSingleObject.restype = wintypes.DWORD

# Win32 constants
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x1
FILE_SHARE_WRITE = 0x2
OPEN_EXISTING = 3
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value
WAIT_OBJECT_0 = 0x00000000
INFINITE = 0xFFFFFFFF


@dataclass
class DeviceIoResult:
    """Result of a DeviceIoControl operation."""
    success: bool
    buffer: KeyStroke | MouseStroke = None


class Device:
    """Represents an input device controlled via the Interception driver."""

    def __init__(self, device_path: str):
        """Initializes an InterceptionDevice with a specific device path.

        Args:
            device_path (str): The device path (e.g., '\\\\.\\interception01').

        Raises:
            RuntimeError: If the device or event handle fails to open or bind.
        """
        self.device_path = device_path
        self.handle = self._open_device()
        self.event = self._create_event()
        self._bind_event()

    def _open_device(self):
        """Opens a handle to the device using CreateFile.

        Returns:
            HANDLE: A valid Windows handle to the device.

        Raises:
            RuntimeError: If the handle is invalid.
        """
        handle = CreateFile(
            self.device_path,
            GENERIC_READ,
            0,
            None,
            OPEN_EXISTING,
            0,
            None
        )
        if handle == INVALID_HANDLE_VALUE:
            raise RuntimeError(f"Failed to open {self.device_path}")
        return handle

    @staticmethod
    def _create_event():
        """Creates a manual-reset event object for signaling device readiness.

        Returns:
            HANDLE: A Windows event handle.

        Raises:
            RuntimeError: If the event creation fails.
        """
        event = CreateEvent(None, True, False, None)  # manual-reset, initially non-signaled
        if not event:
            raise RuntimeError("Failed to create event")
        return event

    def _bind_event(self):
        """Binds the created event to the device.

        Raises:
            RuntimeError: If the event cannot be bound.
        """
        result = self._device_io_control(ioctl_code=IOCTL_SET_EVENT, in_buffer=ctypes.c_void_p(self.event))
        if not result.success:
            raise RuntimeError(f"Failed to bind event for {self.device_path}")

    def wait_for_event(self, timeout_ms=1000):
        """Waits for the device to signal an event.

        Args:
            timeout_ms (int): Timeout in milliseconds. Defaults to 1000ms.

        Returns:
            bool: True if the event was signaled, False if timed out.
        """
        result = WaitForSingleObject(self.event, timeout_ms)
        return result == WAIT_OBJECT_0

    def get_hwid(self):
        """Retrieves the hardware ID string of the device.

        Returns:
            str | None: The hardware ID if successful, otherwise None.
        """
        buffer_size = 512
        out_buffer = (ctypes.c_wchar * buffer_size)()
        result = self._device_io_control(ioctl_code=IOCTL_GET_HARDWARE_ID, out_buffer=out_buffer)

        return ctypes.wstring_at(out_buffer) if result.success else None

    def set_filter(self, value: FilterKeyState | FilterMouseState):
        """Sets a key or mouse filter for this device.

        Args:
            value (FilterKeyState | FilterMouseState): The filter value to set.

        Raises:
            RuntimeError: If setting the filter fails.
        """
        result = self._device_io_control(ioctl_code=IOCTL_SET_FILTER, in_buffer=ctypes.c_ushort(value))
        if not result.success:
            raise RuntimeError(f"Failed to set filter for {self.device_path}")

    def send(self, stroke: KeyStroke | MouseStroke):
        """Sends a keystroke or mouse input to the device.

        Args:
            stroke (KeyStroke | MouseStroke): The input stroke to send.
        """
        return self._device_io_control(ioctl_code=IOCTL_WRITE, in_buffer=stroke)

    def receive(self) -> KeyStroke | MouseStroke | None:
        """Receives a keystroke or mouse input from the device.

        Returns:
            KeyStroke | MouseStroke | None: The received input if successful, otherwise None.

        Raises:
            RuntimeError: If the device is not identified as keyboard or mouse.
        """
        if self.is_keyboard:
            out_buffer = KeyStroke()
        elif self.is_mouse:
            out_buffer = MouseStroke()
        else:
            raise RuntimeError(f"Unsupported device {self.device_path}")

        result = self._device_io_control(ioctl_code=IOCTL_READ, out_buffer=out_buffer)

        return out_buffer if result.success else None

    def close(self):
        """Closes the device and event handles."""
        if self.event:
            CloseHandle(self.event)
            self.event = None
        if self.handle:
            CloseHandle(self.handle)
            self.handle = None

    def _device_io_control(self, ioctl_code, in_buffer=None, out_buffer=None):
        """Internal wrapper for DeviceIoControl calls.

        Args:
            ioctl_code (int): The IOCTL code to send.
            in_buffer: Optional input buffer.
            out_buffer: Optional output buffer.

        Returns:
            DeviceIoResult: Result object with success flag and output buffer.
        """
        bytes_returned = wintypes.DWORD()
        success = DeviceIoControl(
            self.handle,
            ioctl_code,
            ctypes.byref(in_buffer) if in_buffer else None,
            ctypes.sizeof(in_buffer) if in_buffer else 0,
            ctypes.byref(out_buffer) if out_buffer else None,
            ctypes.sizeof(out_buffer) if out_buffer else 0,
            ctypes.byref(bytes_returned),
            None
        )

        return DeviceIoResult(success, out_buffer)

    @property
    def is_keyboard(self):
        """Checks if this device is a keyboard based on its path index.

        Returns:
            bool: True if it's a keyboard device.
        """
        idx = int(self.device_path[-2:])
        return 1 <= idx <= 10

    @property
    def is_mouse(self):
        """Checks if this device is a mouse based on its path index.

        Returns:
            bool: True if it's a mouse device.
        """
        idx = int(self.device_path[-2:])
        return 11 <= idx <= 20
