Hivetrace SDK

Description
Hivetrace SDK is designed for integration with the Hivetrace service, providing monitoring of user prompts and LLM responses.

Installation
Install the SDK via pip:

```bash
pip install hivetrace
```

Usage

```python
from hivetrace.hivetrace import HivetraceSDK
```

## Synchronous and Asynchronous Modes
Hivetrace SDK supports both synchronous and asynchronous execution modes.

### Initialization with Sync/Async Mode
By default, the SDK operates in asynchronous mode. You can explicitly specify the mode during initialization:

```python
# Async mode (default)
hivetrace = HivetraceSDK(async_mode=True)

# Sync mode
hivetrace = HivetraceSDK(async_mode=False)
```

Send a user prompt


```python
# Async mode
response = hivetrace.input_async(
    application_id="your-application-id", # get after registering the application in the UI
    message="User prompt here"
)
# Sync mode
response = hivetrace.input(
    application_id="your-application-id", # get after registering the application in the UI
    message="User prompt here"
)
```

Send a response from your LLM

```python
# Async mode
response = hivetrace.output_async(
    application_id="your-application-id", # get after registering the application in the UI
    message="LLM response here"
)
# Sync mode
response = hivetrace.output(
    application_id="your-application-id", # get after registering the application in the UI
    message="LLM response here"
)
```

Example with additional parameters

```python
response = hivetrace.input(
    application_id="your-application-id", 
    message="User prompt here",
    additional_parameters={
        "session_id": "your-session-id",
        "user_id": "your-user-id",
        "agents": {
            "agent-1-id": {"name": "Agent 1", "description": "Agent description"},
            "agent-2-id": {"name": "Agent 2"},
            "agent-3-id": {}
        }
    }
)
```
`session_id`, `user_id`, `agent_id`  - must be a valid UUID

API

#### `input(application_id: str, message: str, additional_parameters: dict = None) -> dict`
Sends a user prompt to Hivetrace.

- `application_id` - Application identifier (must be a valid UUID, created in the UI)
- `message` - User prompt
- `additional_parameters` - Dictionary of additional parameters (optional)

Response Example:

```json
{
    "status": "processed",
    "monitoring_result": {
        "is_toxic": false,
        "type_of_violation": "benign",
        "token_count": 9,
        "token_usage_warning": false,
        "token_usage_unbounded": false
    }
}
```

#### `output(application_id: str, message: str, additional_parameters: dict = None) -> dict`
Sends an LLM response to Hivetrace.

- `application_id` - Application identifier (must be a valid UUID, created in the UI)
- `message` - LLM response
- `additional_parameters` - Dictionary of additional parameters (optional)

Response Example:

```json
{
    "status": "processed",
    "monitoring_result": {
        "is_toxic": false,
        "type_of_violation": "safe",
        "token_count": 21,
        "token_usage_warning": false,
        "token_usage_unbounded": false
    }
}
```

### Sending Requests in Async Mode
When using async mode, you can send requests asynchronously:

```python
import asyncio

async def main():
    hivetrace = HivetraceSDK(async_mode=True)
    response = await hivetrace.input_async(
        application_id="your-application-id", # get after registering the application in the UI
        message="User prompt here"
    )
    await hivetrace.close()

asyncio.run(main())
```

### Sending Requests in Sync Mode
If you prefer synchronous execution, you can send requests normally:

```python
def main():
    hivetrace = HivetraceSDK(async_mode=False)
    response = hivetrace.input(
        application_id="your-application-id", # get after registering the application in the UI
        message="User prompt here"
    )

main()
```

### Closing the Async Client
When using async mode, remember to close the session when done:

```python
await hivetrace.close()
```

### Configuration
The SDK loads configuration from environment variables. The allowed domain (`HIVETRACE_URL`) and API token (`HIVETRACE_ACCESS_TOKEN`) are automatically retrieved from the environment.

#### Configuration Sources
Hivetrace SDK can retrieve the configuration from the following sources:

**.env File:**

```ini
HIVETRACE_URL=https://your-hivetrace-instance.com
HIVETRACE_ACCESS_TOKEN=your-access-token # get in the UI (API Tokens page)
```

The SDK will automatically load this.

## License
This project is licensed under the Apache License 2.0.