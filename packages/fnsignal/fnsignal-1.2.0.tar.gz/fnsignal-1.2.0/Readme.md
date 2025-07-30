# FNSignal

A simple function signal system for Python that allows functions to communicate with each other through signals.

## Features

- Simple signal sending and receiving
- Support for both synchronous and asynchronous operations
- Callback function support
- Signal filtering by sender

## Installation

```bash
pip install fnsignal
```

## Usage

### Basic Usage

```python
from fnsignal import send_signal, receive_signal

# Send a signal
send_signal("target_function")

# Check if signal was received
if receive_signal("target_function"):
    print("Signal received!")
```

### Using Callbacks

```python
from fnsignal import send_signal, receive_signal, wait_for_signals

def my_callback():
    print("Signal received!")

# Register callback
receive_signal("target_function", my_callback)

# Send signal
send_signal("target_function")

# Wait for all signals to be processed
wait_for_signals()
```

### Asynchronous Usage

```python
import asyncio
from fnsignal import send_signal, receive_signal_async

async def main():
    # Wait for signal asynchronously
    await receive_signal_async("target_function")
    print("Signal received!")

# Send signal
send_signal("target_function")

# Run async function
asyncio.run(main())
```

## License

MIT License 