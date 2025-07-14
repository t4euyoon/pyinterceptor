# PyInterceptor

PyInterceptor is a Python library for intercepting and manipulating keyboard and mouse inputs on Windows systems. It provides a high-level interface for working with keyboard and mouse events, including hotkey management and input simulation.

## Features

- Intercept keyboard and mouse inputs at the system level
- Register and manage hotkeys with custom callbacks
- Simulate keyboard and mouse inputs
- Track the state of pressed keys
- Filter specific types of input events
- Support for both keyboard and mouse devices

## Requirements

- Windows operating system
- Python 3.6+
- Interception driver installed on the system

## Installation

```bash
pip install pyinterceptor-hotkeys
```

## Usage Examples

### Basic Hotkey Registration

```python
from pyinterceptor import HotkeyManager, Key, Device, KeyStroke


def on_hotkey_pressed(device: Device, stroke: KeyStroke, pressed_keys: set[Key]):
    print("Hotkey was pressed!")


# Create a hotkey manager for keyboard and use it as a context manager
with HotkeyManager(keyboard=True) as hotkey_manager:
    # Register Ctrl+Shift+A as a hotkey
    hotkey = hotkey_manager.register_hotkey([Key.LEFT_CTRL, Key.LEFT_SHIFT, Key.A], on_hotkey_pressed)

    # The manager automatically starts listening when entering the 'with' block
    print("Listening for hotkeys... Press Ctrl+Shift+A")

    # Keep the main thread alive to listen for hotkeys
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    # The manager automatically stops listening when exiting the 'with' block
    # To unregister a hotkey (optional, as manager cleans up on exit)
    # hotkey_manager.unregister_hotkey(hotkey)
```

### HotkeyManager without 'with' statement

```python
from pyinterceptor import HotkeyManager, Key, Device, KeyStroke
import time

def on_hotkey_pressed_no_with(device: Device, stroke: KeyStroke, pressed_keys: set[Key]):
    print("Hotkey was pressed (without 'with' statement)!")

# Create a hotkey manager instance
hotkey_manager_no_with = HotkeyManager(keyboard=True)

try:
    # Manually start listening
    hotkey_manager_no_with.listen()
    print("Listening for hotkeys (without 'with' statement)... Press Ctrl+Shift+B")

    # Register Ctrl+Shift+B as a hotkey
    hotkey_no_with = hotkey_manager_no_with.register_hotkey([Key.LEFT_CTRL, Key.LEFT_SHIFT, Key.B], on_hotkey_pressed_no_with)

    # Keep the main thread alive to listen for hotkeys
    while True:
        time.sleep(0.1) # Small delay to prevent busy-waiting
except KeyboardInterrupt:
    pass
finally:
    # Manually stop listening and clean up resources
    if hotkey_manager_no_with:
        hotkey_manager_no_with.close()
    # To unregister a hotkey (optional)
    # hotkey_manager_no_with.unregister_hotkey(hotkey_no_with)
```

### Simulating Keyboard Input

```python
from pyinterceptor import Keyboard, Key

# Create a keyboard instance (device ID 1)
keyboard = Keyboard(device=1)

# Simulate pressing and releasing the 'A' key
keyboard.tap(Key.A)

# Press a key
keyboard.press(Key.B)

# Release a key
keyboard.release(Key.B)
```

### Intercepting Input Events

```python
from pyinterceptor import Interception

# Get the singleton instance of Interception
interception = Interception()

# Set up a filter for keyboard events
interception.set_filter_keyboard()


# Add an event listener
def input_callback(stroke):
    print(f"Key: {stroke.code}, State: {stroke.flags}")
    # Return True to suppress the input, False to let it through
    return False


interception.add_event_listener(input_callback)

# Main event loop
try:
    while True:
        # Wait for and process input events
        interception.receive()
except KeyboardInterrupt:
    # Clean up
    interception.close()
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.