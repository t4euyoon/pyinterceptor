from enum import IntEnum


class Key(IntEnum):
    # ────────── Modifier keys ──────────
    LEFT_SHIFT = 0x2A
    RIGHT_SHIFT = 0x36
    LEFT_CTRL = 0x1D
    RIGHT_CTRL = 0xE01D
    LEFT_ALT = 0x38
    RIGHT_ALT = 0xE038  # AltGr key
    CAPS_LOCK = 0x3A

    # ────────── Alphanumeric keys ──────────
    A = 0x1E
    B = 0x30
    C = 0x2E
    D = 0x20
    E = 0x12
    F = 0x21
    G = 0x22
    H = 0x23
    I = 0x17
    J = 0x24
    K = 0x25
    L = 0x26
    M = 0x32
    N = 0x31
    O = 0x18
    P = 0x19
    Q = 0x10
    R = 0x13
    S = 0x1F
    T = 0x14
    U = 0x16
    V = 0x2F
    W = 0x11
    X = 0x2D
    Y = 0x15
    Z = 0x2C

    NUM_0 = 0x0B
    NUM_1 = 0x02
    NUM_2 = 0x03
    NUM_3 = 0x04
    NUM_4 = 0x05
    NUM_5 = 0x06
    NUM_6 = 0x07
    NUM_7 = 0x08
    NUM_8 = 0x09
    NUM_9 = 0x0A

    SPACE = 0x39
    TAB = 0x0F
    ENTER = 0x1C
    BACKSPACE = 0x0E
    ESC = 0x01

    # ────────── Function keys ──────────
    F1 = 0x3B
    F2 = 0x3C
    F3 = 0x3D
    F4 = 0x3E
    F5 = 0x3F
    F6 = 0x40
    F7 = 0x41
    F8 = 0x42
    F9 = 0x43
    F10 = 0x44
    F11 = 0x57
    F12 = 0x58

    # ────────── Navigation and editing keys ──────────
    INSERT = 0xE052
    DELETE = 0xE053
    HOME = 0xE047
    END = 0xE04F
    PAGE_UP = 0xE049
    PAGE_DOWN = 0xE051
    UP = 0xE048
    DOWN = 0xE050
    LEFT = 0xE04B
    RIGHT = 0xE04D

    PRINT_SCREEN = 0xE037  # Two-part scan code sequence
    SCROLL_LOCK = 0x46
    PAUSE_BREAK = 0xE11D45  # Multi-part scan code

    # ────────── Numpad keys ──────────
    NUMPAD_0 = 0x52
    NUMPAD_1 = 0x4F
    NUMPAD_2 = 0x50
    NUMPAD_3 = 0x51
    NUMPAD_4 = 0x4B
    NUMPAD_5 = 0x4C
    NUMPAD_6 = 0x4D
    NUMPAD_7 = 0x47
    NUMPAD_8 = 0x48
    NUMPAD_9 = 0x49
    NUMPAD_ENTER = 0xE01C
    NUMPAD_PLUS = 0x4E
    NUMPAD_MINUS = 0x4A
    NUMPAD_MULTIPLY = 0x37
    NUMPAD_DIVIDE = 0xE035
    NUMPAD_DECIMAL = 0x53
    NUM_LOCK = 0x45

    # ────────── OEM / Punctuation keys (US layout) ──────────
    SEMICOLON = 0x27  # ':'
    APOSTROPHE = 0x28  # '\''
    GRAVE = 0x29  # '`~'
    COMMA = 0x33  # ',<'
    PERIOD = 0x34  # '.>'
    SLASH = 0x35  # '/?'
    BACKSLASH = 0x2B  # '\|'
    LBRACKET = 0x1A  # '[{'
    RBRACKET = 0x1B  # ']}'
    MINUS = 0x0C  # '-_'
    EQUAL = 0x0D  # '=+'

    # ────────── Extended keys (F13-F24, media keys, etc.) ──────────
    F13 = 0x64
    F14 = 0x65
    F15 = 0x66
    F16 = 0x67
    F17 = 0x68
    F18 = 0x69
    F19 = 0x6A
    F20 = 0x6B
    F21 = 0x6C
    F22 = 0x6D
    F23 = 0x6E
    F24 = 0x76

    MEDIA_NEXT_TRACK = 0xE019
    MEDIA_PREV_TRACK = 0xE010
    MEDIA_STOP = 0xE024
    MEDIA_PLAY_PAUSE = 0xE022

    VOLUME_MUTE = 0xE020
    VOLUME_DOWN = 0xE02E
    VOLUME_UP = 0xE030

    LAUNCH_MAIL = 0xE06C
    LAUNCH_MEDIA = 0xE06D
    LAUNCH_APP1 = 0xE06B
    LAUNCH_APP2 = 0xE021
    BROWSER_HOME = 0xE032
    BROWSER_SEARCH = 0xE065
    BROWSER_FAVORITES = 0xE066
    BROWSER_REFRESH = 0xE067
    BROWSER_STOP = 0xE068
    BROWSER_FORWARD = 0xE069
    BROWSER_BACK = 0xE06A

    LEFT_WINDOWS = 0xE05B
    RIGHT_WINDOWS = 0xE05C
    APP_MENU = 0xE05D  # Context menu key

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Key.{self.name}(0x{self.value:X})>"
