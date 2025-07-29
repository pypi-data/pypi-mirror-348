# Teer Python SDK

[![PyPI - Version](https://img.shields.io/pypi/v/teer.svg)](https://pypi.org/project/teer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/teer.svg)](https://pypi.org/project/teer)

The official Python SDK for [Teer](https://teer.ai), a platform for tracking and analyzing LLM usage across multiple providers including Anthropic, OpenAI, and Google.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Usage Reports](#usage-reports)
- [Billing](#billing)
- [Examples](#examples)
- [Documentation](#documentation)
- [License](#license)

## Installation

```console
pip install teer
```

## Usage

### Initializing the Client

```python
from teer import TeerClient

# Initialize with your API key
client = TeerClient("YOUR_API_KEY")

# Or initialize with a custom base URL (e.g., for development or enterprise deployments)
client = TeerClient(
    api_key="YOUR_API_KEY",
    base_url="https://dev-track.teer.ai"
)
```

### Sending Basic Usage Data

```python
# Send basic usage data
client.ingest.send({
    # Required: Specify the LLM provider
    "provider": "anthropic",

    # Required: Specify the model name
    "model": "claude-3-haiku-20240307",

    # Optional: A unique identifier for the function or endpoint using the LLM
    "function_id": "summarize-article",

    # Required: Token usage information
    "usage": {
        # Number of input tokens
        "input": 1000,
        # Number of output tokens
        "output": 2000
    }
})
```

## Usage Reports

Teer supports detailed usage reports for different LLM providers. Here are some examples of more advanced usage reports:

### Usage Reports with Cache Information

#### Anthropic Cache

```python
client.ingest.send({
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "function_id": "legal-document-analysis",
    "usage": {
        "input": 2000,
        "output": 3000,
        # Anthropic-specific cache information
        "cache": {
            "anthropic": {
                # Tokens used to create the cache
                "cache_creation_input_tokens": 1500,
                # Tokens read from the cache
                "cache_read_input_tokens": 500
            }
        }
    }
})
```

#### OpenAI Cache

```python
client.ingest.send({
    "provider": "openai",
    "model": "gpt-4o",
    "function_id": "code-generation",
    "usage": {
        "input": 800,
        "output": 2500,
        # OpenAI-specific cache information
        "cache": {
            "openai": {
                # Tokens retrieved from cache
                "input_cached_tokens": 300
            }
        }
    }
})
```

#### Google Cache

```python
client.ingest.send({
    "provider": "google",
    "model": "gemini-ultra",
    "function_id": "image-analysis",
    "usage": {
        "input": 1200,
        "output": 1800,
        # Google-specific cache information
        "cache": {
            "google": {
                # Tokens retrieved from cache
                "cached_content_token_count": 800,
                # Tokens used for thoughts
                "thoughts_token_count": 400
            }
        }
    }
})
```

### Usage Report with User Attribution

```python
client.ingest.send({
    "provider": "openai",
    "model": "gpt-4o-mini-2024-07-18",
    "function_id": "generate-content",
    "usage": {
        "input": 500,
        "output": 1500
    },
    # Metadata for user attribution and analytics
    "metadata": {
        # User identification
        "user_id": "user-123456",
        "organization_id": "org-abcdef",

        # Session information
        "session_id": "session-xyz789"
    }
})
```

### Usage Report Without Function ID

```python
client.ingest.send({
    # Required: Specify the LLM provider
    "provider": "google",

    # Required: Specify the model name
    "model": "gemini-2.0-flash-001",

    # function_id is optional and can be omitted

    # Required: Token usage information
    "usage": {
        "input": 400,
        "output": 1200
    }
})
```

For a complete reference of all supported fields in usage reports, see the [Usage Reports documentation](./docs/usage_reports.md).

## Billing

Teer provides a billing resource for usage-based billing integration with providers like Stripe.

### Creating Meter Events

```python
from teer import TeerClient
from datetime import datetime, UTC

# Initialize the client with your API key
client = TeerClient("YOUR_API_KEY")

# Get the current timestamp in ISO 8601 format using timezone-aware approach
current_timestamp = datetime.now(UTC).isoformat()

# Create a meter event
meter_event = client.billing.meter_events.create({
    "provider": "stripe",
    "fields": {
        "identifier": "idmp_12345678",
        "event_name": "ai_search_api",
        "timestamp": current_timestamp,
        "payload": {
            "stripe_customer_id": "cus_12345678",
            "value": "25",
        },
    },
})
```

## Examples

Check out the [examples](./examples) directory for more usage examples:

- [Basic Usage](./examples/basic_usage.py): Simple example of using the Teer client
- [Custom Base URL](./examples/custom_base_url.py): Example of initializing the Teer client with a custom base URL
- [Comprehensive Usage Reports](./examples/comprehensive_usage_reports.py): Detailed examples of various usage report scenarios
- [Usage Payload Example](./examples/usage_payload_example.py): Example of creating a payload for the Teer ingest API
- [Billing Meter Events](./examples/billing_meter_events.py): Example of creating meter events for usage-based billing

## Documentation

Detailed documentation is available in the [docs](./docs) directory:

- [Usage Reports](./docs/usage_reports.md): Detailed information about the structure and fields of usage reports

## License

`teer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Publishing
```
python scripts/publish.py patch

python scripts/publish.py minor

python scripts/publish.py major
```
