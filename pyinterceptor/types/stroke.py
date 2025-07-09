from ctypes import Structure, c_ushort, c_ulong, c_long

from . import Key, KeyState


class KeyStroke(Structure):
    """Represents a keyboard input stroke structure compatible with interception driver.

    Attributes:
        unit_id (c_ushort): Device unit identifier.
        _code (c_ushort): Scan code of the key.
        _flags (c_ushort): Flags describing key state and extensions.
        reserved (c_ushort): Reserved field, unused.
        information (c_ulong): Additional information, zero indicates hardware input.
    """

    _fields_ = [
        ("unit_id", c_ushort),
        ("_code", c_ushort),
        ("_flags", c_ushort),
        ("reserved", c_ushort),
        ("information", c_ulong),
    ]

    information: int

    # Mapping from extension flags to high byte prefix for full key code
    _EXT_PREFIX_MAP = {
        KeyState.E0: 0xE000,
        KeyState.E1: 0xE100,
    }
    # Reverse mapping from prefix to extension flag
    _EXT_PREFIX_MAP_INV = {
        0xE000: KeyState.E0,
        0xE100: KeyState.E1,
    }

    def __init__(self, code: Key | int = 0, flags: KeyState | int = KeyState.DOWN, information: int = 0):
        """
        Initializes a KeyStroke structure.

        Args:
            code (Key | int, optional): Key code including extension prefix.
            flags (KeyState | int, optional): Key state flags. Defaults to KeyState.DOWN.
            information (int, optional): Information field. 0 indicates hardware. Defaults to 0.
        """
        super().__init__()  # Ensures structure memory is correctly initialized

        self.code = code  # goes through @code.setter
        self.flags = flags  # goes through @flags.setter
        self.information = information

    def __repr__(self):
        return f"KeyStroke(code={self.code}, flags={self.flags}, information={self.information})"

    @property
    def code(self) -> Key:
        """Gets the full key code including extension prefix if applicable.

        Returns:
            Key: The full key code combining prefix and base code.
        """
        prefix = 0
        # Check for E0/E1 extension flags and determine prefix
        for flag, prefix_val in self._EXT_PREFIX_MAP.items():
            if self.flags & flag:
                prefix = prefix_val
                break
        full_code = prefix | self._code
        return Key(full_code)

    @code.setter
    def code(self, value: Key | int):
        """Sets the key code and updates flags based on extension prefix.

        Args:
            value (Key | int): The key code to set, either as Key enum or int.

        Raises:
            TypeError: If value is not int or Key.
        """
        if isinstance(value, Key):
            code_val = value.value
        elif isinstance(value, int):
            code_val = value
        else:
            raise TypeError("code must be int or Key enum")

        prefix = code_val & 0xFF00
        base_code = code_val & 0x00FF

        # Clear existing extension flags
        self._flags &= ~(KeyState.E0 | KeyState.E1)

        # Set extension flags based on prefix
        if prefix in self._EXT_PREFIX_MAP_INV:
            self._flags |= self._EXT_PREFIX_MAP_INV[prefix]

        self._code = base_code

    @property
    def flags(self) -> KeyState:
        """Gets the key state flags.

        Returns:
            KeyState: The flags representing key state and extensions.
        """
        return KeyState(self._flags)

    @flags.setter
    def flags(self, value: KeyState | int):
        """Sets the key state flags.

        Args:
            value (KeyState | int): Flags to set.

        Raises:
            TypeError: If value is not int or KeyState.
        """
        if isinstance(value, KeyState):
            self._flags = value.value
        elif isinstance(value, int):
            self._flags = value
        else:
            raise TypeError("flags must be int or KeyState enum")

    @property
    def is_down(self) -> bool:
        """Indicates if the key is currently pressed down.

        Returns:
            bool: True if key is down, False if key is up.
        """
        return not bool(self.flags & KeyState.UP)

    @property
    def is_hardware(self) -> bool:
        """Indicates if the input is from hardware (not software).

        Returns:
            bool: True if hardware input, False otherwise.
        """
        return not bool(self.information)


class MouseStroke(Structure):
    """Represents a mouse input stroke structure compatible with interception driver.

    Attributes:
        unit_id (c_ushort): Device unit identifier.
        flags (c_ushort): General mouse input flags.
        button_flags (c_ushort): Mouse button specific flags.
        button_data (c_ushort): Additional data for buttons (e.g. wheel delta).
        raw_buttons (c_ulong): Raw button data.
        x (c_long): Movement in X axis.
        y (c_long): Movement in Y axis.
        information (c_ulong): Additional information, zero indicates hardware input.
    """

    _fields_ = [
        ("unit_id", c_ushort),
        ("flags", c_ushort),
        ("button_flags", c_ushort),
        ("button_data", c_ushort),
        ("raw_buttons", c_ulong),
        ("x", c_long),
        ("y", c_long),
        ("information", c_ulong),
    ]

    flags: int
    button_flags: int
    button_data: int
    x: int
    y: int
    information: int

    def __repr__(self):
        return (f"MouseStroke(flags={self.flags}, button_flags={self.button_flags}, button_data={self.button_data},"
                f" x={self.x}, y={self.y}, information={self.information})")
