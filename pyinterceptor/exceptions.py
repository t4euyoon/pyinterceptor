class InterceptionError(Exception):
    ...


# Low-level driver-related
class DriverLoadError(InterceptionError):
    ...


class DeviceNotFoundError(InterceptionError):
    ...


class UnsupportedDeviceError(InterceptionError):
    ...


class DeviceIoError(InterceptionError):
    ...


# Input & logic
class UnsupportedInputTypeError(InterceptionError):
    ...


class NotInitializedError(InterceptionError):
    ...


# Hotkey-related
class HotkeyError(Exception):
    ...


class HotkeyConflictError(HotkeyError):
    ...


class HotkeyNotFoundError(HotkeyError):
    ...
