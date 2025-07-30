# traceloggerx
✨ A Python logging utility with colorful console output and structured JSON file logging. Built for real-world debugging and traceability.


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


## License
MIT
