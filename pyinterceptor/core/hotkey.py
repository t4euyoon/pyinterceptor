import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, Set

from . import Interception, InputStateManager
from ..types import Key

CallbackType = Callable[[set[Key]], None]


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

    def run_callback(self, pressed_keys: Set[Key] = None) -> bool:
        """Runs the callback function and resets running state.

        Args:
            pressed_keys (Set[Key], optional): Currently pressed keys, passed to callback.

        Returns:
            bool: The is_suppress flag indicating whether to suppress input.
        """
        try:
            self.callback(pressed_keys)
            return self.is_suppress
        finally:
            self.is_running = False


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
        # self.hotkeys: Dict[int, Hotkey] = {}
        self.hotkeys: set[Hotkey] = set()

        self._executor = ThreadPoolExecutor()
        self.interception = Interception()
        self.input_state_manager = InputStateManager()

        if keyboard:
            self.interception.set_filter_keyboard()
        if mouse:
            self.interception.set_filter_mouse()

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

    def process_key_event(self, _) -> bool:
        """Processes a key event from intercepted input.

        Checks all registered hotkeys against current hardware key states,
        triggers callbacks asynchronously if matched.

        Args:
            _ : Unused parameter (input stroke).

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
                self._executor.submit(hotkey.run_callback, pressed_keys)

        return is_suppress

    def listen(self):
        """Continuously listens for input events and logs them.

        This method blocks indefinitely.
        """
        while True:
            result = self.interception.receive()
            logging.debug(result)
