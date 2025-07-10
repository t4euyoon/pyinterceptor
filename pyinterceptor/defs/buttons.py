from enum import Enum

from . import MouseState


class MouseButton(Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    BUTTON_4 = "button_4"
    BUTTON_5 = "button_5"

    def __new__(cls, value):
        # str로 선언된 Enum 생성일 경우 그대로 사용
        if isinstance(value, str):
            return super().__new__(cls, value)

        # MouseState 또는 int로 전달된 경우 매핑 시도
        if isinstance(value, MouseState) or isinstance(value, int):
            value = MouseState(value)
            for flag, button in cls._mouse_state_to_button_map().items():
                if value & flag:
                    return super().__new__(cls, button.value)

        raise ValueError(f"Cannot convert {value!r} to MouseButton")

    @property
    def down(self) -> MouseState:
        return {
            MouseButton.LEFT: MouseState.LEFT_BUTTON_DOWN,
            MouseButton.RIGHT: MouseState.RIGHT_BUTTON_DOWN,
            MouseButton.MIDDLE: MouseState.MIDDLE_BUTTON_DOWN,
            MouseButton.BUTTON_4: MouseState.BUTTON_4_DOWN,
            MouseButton.BUTTON_5: MouseState.BUTTON_5_DOWN,
        }[self]

    @property
    def up(self) -> MouseState:
        return {
            MouseButton.LEFT: MouseState.LEFT_BUTTON_UP,
            MouseButton.RIGHT: MouseState.RIGHT_BUTTON_UP,
            MouseButton.MIDDLE: MouseState.MIDDLE_BUTTON_UP,
            MouseButton.BUTTON_4: MouseState.BUTTON_4_UP,
            MouseButton.BUTTON_5: MouseState.BUTTON_5_UP,
        }[self]

    @classmethod
    def _mouse_state_to_button_map(cls) -> dict[MouseState, "MouseButton"]:
        return {
            MouseState.LEFT_BUTTON_DOWN: cls.LEFT,
            MouseState.LEFT_BUTTON_UP: cls.LEFT,
            MouseState.RIGHT_BUTTON_DOWN: cls.RIGHT,
            MouseState.RIGHT_BUTTON_UP: cls.RIGHT,
            MouseState.MIDDLE_BUTTON_DOWN: cls.MIDDLE,
            MouseState.MIDDLE_BUTTON_UP: cls.MIDDLE,
            MouseState.BUTTON_4_DOWN: cls.BUTTON_4,
            MouseState.BUTTON_4_UP: cls.BUTTON_4,
            MouseState.BUTTON_5_DOWN: cls.BUTTON_5,
            MouseState.BUTTON_5_UP: cls.BUTTON_5,
        }
