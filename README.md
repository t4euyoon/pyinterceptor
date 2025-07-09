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
pip install pyinterceptor
```

## Usage Examples

### Basic Hotkey Registration

```python
from pyinterceptor import HotkeyManager
from pyinterceptor.types import Key

def on_hotkey_pressed():
    print("Hotkey was pressed!")

# Create a hotkey manager for keyboard
hotkey_manager = HotkeyManager(keyboard=True)

# Register Ctrl+Shift+A as a hotkey
hotkey = hotkey_manager.register_hotkey([Key.LEFT_CTRL, Key.LEFT_SHIFT, Key.A], on_hotkey_pressed)

# Start listening for hotkeys
hotkey_manager.listen()

# To unregister a hotkey
# hotkey_manager.unregister_hotkey(hotkey)
```

### Simulating Keyboard Input

```python
from pyinterceptor import Keyboard
from pyinterceptor.types import Key

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
from pyinterceptor.types import KeyState

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