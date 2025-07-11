import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Set

from pyinterceptor.core import Device, CallbackType
from pyinterceptor.defs import Key, KeyStroke, MouseStroke, FilterKeyState, FilterMouseState
from pyinterceptor.utils import decorators


class Hotkey:
    """Represents a hotkey combination with an associated callback.

    Attributes:
        keys (Set[Key]): The set of keys that activate this hotkey.
        callback (Callable): Function to call when hotkey is triggered.
        allow_reentry (bool): Whether the callback can be reentered if still running.
        is_running (bool): Indicates if the callback is currently running.
        is_suppress (bool): Whether to suppress input events when triggered.
    """

    def __init__(self, keys: Set[Key], callback: CallbackType, allow_reentry: bool = False, is_suppress: bool = True):
        """Initializes the hotkey with keys, callback and behavior flags.

        Args:
            keys (Set[Key]): Keys composing the hotkey.
            callback (Callable): Callback to invoke on hotkey press.
            allow_reentry (bool): Allow callback to run concurrently if True.
            is_suppress (bool): Suppress input events when hotkey triggers.
        """
        self.keys = keys
        self.callback = callback
        self.allow_reentry = allow_reentry
        self.is_suppress = is_suppress

        self.is_running = False

    def matches(self, pressed_keys: Set[Key]) -> bool:
        """Checks if this hotkey's keys are a subset of the currently pressed keys.

        Args:
            pressed_keys (Set[Key]): Currently pressed hardware keys.

        Returns:
            bool: True if hotkey matches pressed keys, False otherwise.
        """
        return self.keys <= pressed_keys

    def run_callback(self, device: Device, stroke: KeyStroke | MouseStroke, pressed_keys: Set[Key]) -> bool:
        """Runs the callback function and resets running state.

        Args:
            device (Device): The device on which the hotkey was triggered.
            stroke (KeyStroke | MouseStroke): The input stroke that triggered the hotkey.
            pressed_keys (Set[Key]): The set of hardware keys currently pressed at the moment of triggering.

        Returns:
            bool: The is_suppress flag indicating whether to suppress input.
        """
        try:
            self.callback(device, stroke, pressed_keys)
            return self.is_suppress
        finally:
            self.is_running = False


@decorators.singleton
class HotkeyManager:
    """Manages multiple hotkeys and dispatches callbacks on matching input events.

    Attributes:
        hotkeys (Dict[int, Hotkey]): Registered hotkeys indexed by ID.
        _executor (ThreadPoolExecutor): Thread pool for running hotkey callbacks asynchronously.
    """

    def __init__(self, keyboard: bool = True, mouse: bool = False):
        """Initializes the manager, optionally enabling keyboard and mouse interception.

        Args:
            keyboard (bool): Enable keyboard input interception (default True).
            mouse (bool): Enable mouse input interception (default False).
        """
        self._listening = False
        self.hotkeys: set[Hotkey] = set()

        self._executor = ThreadPoolExecutor()

        from pyinterceptor.core import Interception, InputStateManager
        self.interception = Interception()
        self.input_state_manager = InputStateManager()

        self._filter_keyboard = keyboard
        self._filter_mouse = mouse

        self.interception.add_event_listener(self.process_key_event)

    def register_hotkey(self, keys: list[Key], callback: CallbackType, allow_reentry=False) -> Hotkey:
        """Registers a new hotkey with the given keys and callback.

        Args:
            keys (list[Key]): List of keys composing the hotkey.
            callback (Callable): Function to call when hotkey triggers.
            allow_reentry (bool): Allow callback reentry if still running (default False).

        Returns:
            tuple[int, Hotkey]: The unique hotkey ID and the Hotkey instance.
        """
        hotkey = Hotkey(set(keys), callback, allow_reentry)
        self.hotkeys.add(hotkey)

        return hotkey

    def unregister_hotkey(self, hotkey: Hotkey) -> None:
        """Unregisters a hotkey by its ID or Hotkey instance.

        Args:
            hotkey (int | Hotkey): The ID of the hotkey to remove, or the Hotkey instance itself.
        """
        self.hotkeys.discard(hotkey)

    def process_key_event(self, device: Device, stroke: KeyStroke | MouseStroke) -> bool:
        """Processes a key event from intercepted input.

        Checks all registered hotkeys against current hardware key states,
        triggers callbacks asynchronously if matched.

        Args:
            device (Device): The device instance generating the event.
            stroke (KeyStroke | MouseStroke): The input stroke event.

        Returns:
            bool: True if any hotkey suppresses the input, False otherwise.
        """
        pressed_keys = self.input_state_manager.pressed_hardware_keys
        is_suppress = False

        for hotkey in self.hotkeys:
            if not hotkey.matches(pressed_keys):
                continue

            is_suppress |= hotkey.is_suppress
            if not hotkey.is_running or hotkey.allow_reentry:
                # Mark callback running and schedule it on thread pool
                hotkey.is_running = True
                self._executor.submit(hotkey.run_callback, device, stroke, pressed_keys)

        return is_suppress

    def listen(self):
        """Continuously listens for input events and logs them.

        This method blocks indefinitely.
        """
        if self._filter_keyboard:
            self.interception.set_filter_keyboard()
        if self._filter_mouse:
            self.interception.set_filter_mouse()

        self._listening = True

        while self._listening:
            self.interception.receive()

    def toggle_filter_keyboard(self, toggle: bool | None = None):
        """Toggle keyboard filter state.

        Args:
            toggle (bool | None): If given, set filter to this value; otherwise toggle current state.
        """
        self._filter_keyboard = toggle if toggle is not None else not self._filter_keyboard
        self.interception.set_filter_keyboard(FilterKeyState.NONE if self._filter_keyboard else FilterKeyState.ALL)

    def toggle_filter_mouse(self, toggle: bool | None = None):
        """Toggle mouse filter state.

        Args:
            toggle (bool | None): If given, set filter to this value; otherwise toggle current state.
        """
        self._filter_mouse = toggle if toggle is not None else not self._filter_mouse
        self.interception.set_filter_mouse(FilterMouseState.NONE if self._filter_mouse else FilterMouseState.ALL)