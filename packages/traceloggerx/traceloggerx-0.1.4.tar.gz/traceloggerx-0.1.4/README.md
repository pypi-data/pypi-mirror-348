# traceloggerx
✨ A Python logging utility with colorful console output and structured JSON file logging. Built for real-world debugging and traceability.

[![PyPI version](https://badge.fury.io/py/traceloggerx.svg)](https://pypi.org/project/traceloggerx/)


## Features
- Colorful console logs using `colorlog`
- JSON structured logs with `trace_id` and `user_id`
- Automatic exception capturing via `sys.excepthook`
- Easily reusable across different projects


## Installation
```bash
pip install traceloggerx
```


## Usage
```python
from logutils.logger import set_logger

# Create a logger with a default user_id
logger = set_logger("myapp", json_format=True, extra={"user_id": "anonymous"})

# Add a trace_id dynamically when logging
logger.info("User accessed dashboard", extra={"trace_id": "req-001"})
```

## Example Usage of `traceloggerx`
This directory contains example scripts demonstrating how to use the `traceloggerx` logging utility.

### Files
- **basic_usage.py**
  Shows the simplest use of the logger with no trace_id or user_id.
- **with_trace_and_user.py**
  Demonstrates how to include custom fields like `trace_id` and `user_id`.
- **fastapi_example.py**
  Integrates `traceloggerx` with a FastAPI web server using middleware.

### How to Run
You can run any script directly:
```bash
python examples/basic_usage.py
```

## License
MIT


## Maintainer
🔗 GitHub: [@darams4863](https://github.com/darams4863/traceloggerx)
📦 PyPI: [traceloggerx](https://pypi.org/project/traceloggerx/)