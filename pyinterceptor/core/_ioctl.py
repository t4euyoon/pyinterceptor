def ctl_code(device_type: int, func: int, method: int, access: int) -> int:
    """Generates a control code (IOCTL) for use with DeviceIoControl.

    This function mimics the Windows CTL_CODE macro used to construct
    device-specific IOCTL codes.

    Args:
        device_type (int): The device type (e.g., FILE_DEVICE_UNKNOWN).
        func (int): The function code for the IOCTL operation.
        method (int): The method of data transfer (e.g., METHOD_BUFFERED).
        access (int): The required access type (e.g., FILE_ANY_ACCESS).

    Returns:
        int: A 32-bit IOCTL control code.
    """
    return (device_type << 16) | (access << 14) | (func << 2) | method


# Constants for use in CTL_CODE
FILE_DEVICE_UNKNOWN = 0x22 # Generic device type
METHOD_BUFFERED     = 0x0  # Data is buffered
FILE_ANY_ACCESS     = 0x0  # No specific access permission required

# IOCTL control codes (function values follow Interception convention)
SET_PRECEDENCE  = ctl_code(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)
GET_PRECEDENCE  = ctl_code(FILE_DEVICE_UNKNOWN, 0x802, METHOD_BUFFERED, FILE_ANY_ACCESS)
SET_FILTER      = ctl_code(FILE_DEVICE_UNKNOWN, 0x804, METHOD_BUFFERED, FILE_ANY_ACCESS)
GET_FILTER      = ctl_code(FILE_DEVICE_UNKNOWN, 0x808, METHOD_BUFFERED, FILE_ANY_ACCESS)
SET_EVENT       = ctl_code(FILE_DEVICE_UNKNOWN, 0x810, METHOD_BUFFERED, FILE_ANY_ACCESS)
WRITE           = ctl_code(FILE_DEVICE_UNKNOWN, 0x820, METHOD_BUFFERED, FILE_ANY_ACCESS)
READ            = ctl_code(FILE_DEVICE_UNKNOWN, 0x840, METHOD_BUFFERED, FILE_ANY_ACCESS)
GET_HARDWARE_ID = ctl_code(FILE_DEVICE_UNKNOWN, 0x880, METHOD_BUFFERED, FILE_ANY_ACCESS)

