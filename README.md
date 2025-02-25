# Secret AI SDK

[![PyPI version](https://img.shields.io/pypi/v/secret-ai-sdk.svg)](https://pypi.org/project/secret-ai-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/secret-ai-sdk.svg)](https://pypi.org/project/secret-ai-sdk/)
[![License](https://img.shields.io/github/license/scrtlabs/secret-ai-sdk.svg)](https://opensource.org/licenses/MIT)

The Secret AI SDK provides a simple and convenient way to access Secret Confidential AI models. With this SDK, you can easily integrate Secret's AI capabilities into your own applications and services.

## Overview

The Secret AI SDK is a Python library that enables access to Secret Confidential AI models. The SDK provides a simple and intuitive API that allows you to send requests to Secret's AI models and receive responses in a variety of formats.

## Features

- Access to Secret Confidential AI models via a clean, Pythonic interface
- Simple authentication through API keys
- Support for streaming responses
- Flexible model selection and configuration
- Automatic handling of connections to the Secret Network

## Requirements

`secret-ai-sdk` has dependencies specified in the `pyproject.toml` file, with one external dependency:

- You may need to install `secret-sdk` separately:
  ```bash
  pip install 'secret-sdk>=1.8.1'
  ```

## Installation

To install the Secret AI SDK:

```bash
pip install secret-ai-sdk
```

## Usage

### Basic Usage

```python
from secret_ai_sdk.secret_ai import ChatSecret
from secret_ai_sdk.secret import Secret

# Initialize the Secret client
secret_client = Secret()

# Get all models registered with the smart contracts
models = secret_client.get_models()

# For your chosen model, get a list of LLM instance URLs
urls = secret_client.get_urls(model=models[0])

# Create the AI client with specific parameters
secret_ai_llm = ChatSecret(
    base_url=urls[0],  # Choose a specific URL
    model=models[0],    # Your selected model
    temperature=1.0
)

# Define your messages
messages = [
    ("system", "You are a helpful assistant that translates English to French."),
    ("human", "I love programming."),
]

# Invoke the LLM (with streaming disabled)
response = secret_ai_llm.invoke(messages, stream=False)
print(response.content)
```

### API Key

To use the Secret AI SDK, you need your own Secret AI API Key. Visit SecreAI Development portal: [https://aidev.scrtlabs.com/](https://aidev.scrtlabs.com/).

Set your API key as an environment variable:

```bash
export SECRET_AI_API_KEY='YOUR_API_KEY'
```

### Node URL Configuration

If you experience issues with the default node URL, you can manually specify one:

```python
from secret_ai_sdk.secret import Secret

# Option 1: Directly in code
secret_client = Secret(chain_id='pulsar-3', node_url='YOUR_LCD_NODE_URL')

# Option 2: Using an environment variable
# export SECRET_NODE_URL='YOUR_LCD_NODE_URL'
```

For available endpoints and LCD nodes, see the [Secret Network Documentation](https://docs.scrt.network/secret-network-documentation/development/resources-api-contract-addresses/connecting-to-the-network/testnet-pulsar-3).

## Examples

For streaming implementation examples, refer to the `example.py` file included in the package.

## API Documentation

For comprehensive API documentation, please visit our [official documentation](https://docs.scrt.network/secret-network-documentation/secret-ai/sdk).

## License

The Secret AI SDK is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/scrtlabs/secret-ai-sdk/issues) on our GitHub repository.