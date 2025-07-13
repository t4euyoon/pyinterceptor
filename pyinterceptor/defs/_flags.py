from enum import IntFlag


# Reference: https://github.com/oblitum/Interception/blob/master/library/interception.h

class FlagStrMixin:
    """Mixin providing __str__ and __repr__ for IntFlag enums."""

    @classmethod
    def _zero_flag(cls) -> IntFlag | None:
        """Return the enum member whose value is exactly 0, if defined."""
        members = getattr(cls, "__members__", {})
        for name, member in members.items():
            if member.value == 0:
                return member
        return None

    def __str__(self) -> str:
        zero_flag = self._zero_flag()

        if zero_flag is not None and self == zero_flag:
            return zero_flag.name

        members = getattr(self.__class__, "__members__", {})
        flags = [
            name for name, member in members.items()
            if member.value != 0 and member in self
        ]
        return "|".join(flags) if flags else "UNKNOWN"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"


class FilterKeyState(FlagStrMixin, IntFlag):
    """Bit flags for filtering keyboard input events in the interception driver."""
    NONE = 0x0000

    DOWN = 0x0001  # Key pressed down
    UP = 0x0002  # Key released
    E0 = 0x0004  # Extended key flag E0
    E1 = 0x0008  # Extended key flag E1

    TERMSRV_SET_LED = 0x0010  # Terminal server set LED flag
    TERMSRV_SHADOW = 0x0020  # Terminal server shadowing flag
    TERMSRV_VKPACKET = 0x0040  # Terminal server virtual key packet

    ALL = 0xFFFF  # All filter flags enabled


class FilterMouseState(FlagStrMixin, IntFlag):
    """Flags representing mouse filter states for interception driver."""
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

    WHEEL = 0x0400  # Vertical wheel movement
    HWHEEL = 0x0800  # Horizontal wheel movement
    MOVE = 0x1000  # Mouse move events

    ALL = 0xFFFF  # All filter flags enabled


class KeyState(FlagStrMixin, IntFlag):
    """Flags representing the state of a keyboard key in an input stroke."""
    DOWN = 0x00  # Key pressed down (default)
    UP = 0x01  # Key released
    E0 = 0x02  # Extended key flag E0
    E1 = 0x04  # Extended key flag E1

    TERMSRV_SET_LED = 0x08  # Terminal server set LED flag
    TERMSRV_SHADOW = 0x10  # Terminal server shadowing flag
    TERMSRV_VKPACKET = 0x20  # Terminal server virtual key packet


class MouseState(FlagStrMixin, IntFlag):
    """Flags representing the state of mouse buttons and wheel in an input stroke."""
    NONE = 0x000

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

    WHEEL = 0x400  # Vertical wheel movement
    HWHEEL = 0x800  # Horizontal wheel movement


class MouseFlag(FlagStrMixin, IntFlag):
    """Flags controlling mouse input behavior when sending events through Interception."""
    MOVE_RELATIVE = 0x0000  # Mouse movement is relative (default behavior)
    MOVE_ABSOLUTE = 0x0001  # Mouse movement is absolute (screen coordinates)
    VIRTUAL_DESKTOP = 0x0002  # Use entire virtual desktop for absolute coordinates
    ATTRIBUTES_CHANGED = 0x0004  # Indicates mouse attributes have changed
    MOVE_NOCOALESCE = 0x0008  # Prevents coalescing of mouse movement events
    TERMSRV_SRC_SHADOW = 0x0100  # Input originated from terminal services shadowing
