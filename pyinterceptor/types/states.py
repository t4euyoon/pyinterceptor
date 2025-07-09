from enum import IntFlag


# https://github.com/oblitum/Interception/blob/master/library/interception.h

class FilterKeyState(IntFlag):
    """Bit flags for filtering keyboard input events in the interception driver.

    Each flag corresponds to a specific key event or special condition.
    """
    NONE = 0x0000

    DOWN = 0x0001               # Key pressed down
    UP = 0x0002                 # Key released
    E0 = 0x0004                 # Extended key flag E0
    E1 = 0x0008                 # Extended key flag E1

    TERMSRV_SET_LED = 0x0010    # Terminal server set LED flag
    TERMSRV_SHADOW = 0x0020     # Terminal server shadowing flag
    TERMSRV_VKPACKET = 0x0040   # Terminal server virtual key packet

    ALL = 0xFFFF                # All filter flags enabled


class FilterMouseState(IntFlag):
    """Flags representing mouse filter states for interception driver.

    These flags specify which mouse events to intercept or ignore.
    """
    NONE = 0x0000

    LEFT_BUTTON_DOWN = 0x0001
    LEFT_BUTTON_UP = 0x0002
    RIGHT_BUTTON_DOWN = 0x0004
    RIGHT_BUTTON_UP = 0x0008
    MIDDLE_BUTTON_DOWN = 0x0010
    MIDDLE_BUTTON_UP = 0x0020

    BUTTON_4_DOWN = 0x0040
    BUTTON_4_UP = 0x0080
    BUTTON_5_DOWN = 0x0100
    BUTTON_5_UP = 0x0200

    WHEEL = 0x0400             # Vertical wheel movement
    HWHEEL = 0x0800            # Horizontal wheel movement

    MOVE = 0x1000              # Mouse move events
    ALL = 0xFFFF               # All filter flags enabled


class KeyState(IntFlag):
    """Flags representing the state of a keyboard key in an input stroke.

    Used to interpret the status of a key event.
    """
    DOWN = 0x00                # Key pressed down (default)
    UP = 0x01                  # Key released
    E0 = 0x02                  # Extended key flag E0
    E1 = 0x04                  # Extended key flag E1

    TERMSRV_SET_LED = 0x08     # Terminal server set LED flag
    TERMSRV_SHADOW = 0x10      # Terminal server shadowing flag
    TERMSRV_VKPACKET = 0x20    # Terminal server virtual key packet

    def __str__(self):
        """Return a string representation of the key state flags."""
        # If exactly DOWN (0), return it
        if self == KeyState.DOWN:
            return "DOWN"

        # Otherwise list all bits set (excluding DOWN)
        flags: list = [flag.name for flag in KeyState if flag != KeyState.DOWN and flag in self]
        return "|".join(flags) if flags else "UNKNOWN"

    def __repr__(self):
        return f"<KeyState: {str(self)}>"


class MouseState(IntFlag):
    """Flags representing the state of mouse buttons and wheel in an input stroke."""
    LEFT_BUTTON_DOWN = 0x001
    LEFT_BUTTON_UP = 0x002
    RIGHT_BUTTON_DOWN = 0x004
    RIGHT_BUTTON_UP = 0x008
    MIDDLE_BUTTON_DOWN = 0x010
    MIDDLE_BUTTON_UP = 0x020

    BUTTON_4_DOWN = 0x040
    BUTTON_4_UP = 0x080
    BUTTON_5_DOWN = 0x100
    BUTTON_5_UP = 0x200

    WHEEL = 0x400       # Vertical wheel movement
    HWHEEL = 0x800      # Horizontal wheel movement
