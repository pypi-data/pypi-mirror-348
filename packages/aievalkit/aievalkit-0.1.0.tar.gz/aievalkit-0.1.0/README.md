# EvalKit Core Library

This directory contains the core Python library for EvalKit.

## Installation

To install the EvalKit core library:

```bash
pip install evalkit
```

For development, you can install from this directory:

```bash
cd core
pip install -e .
```

## Usage

Import the necessary components from the `core` package (after installing `evalkit`):

```python
from core.kit import EvalKit
from core.models import Span, Task # etc.
# You might also import storage modules if needed directly
# from core.storage import MemoryStorage, HttpStorage

eval_kit = EvalKit() # Uses MemoryStorage by default

@eval_kit.trace_interaction(
        agent_name="agentX",
        prompt_template_arg_name="prompt_template"
)
def agent_function(prompt_template):
    pass

# Example using tracing:
with eval_kit.trace_task(task_name="My Task") as task_ctx:
    # Your agent code here, using @eval_kit.trace_interaction
    pass

# Example using models (if needed separately):
# my_span = Span(...)
# my_task = Task(...)
```

Refer to the main project README for more detailed examples and context within the full EvalKit application. 