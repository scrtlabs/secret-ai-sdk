# Secret AI SDK

The Secret AI SDK provides a simple and convenient way to access Secret Confidential AI models. With this SDK, you can easily integrate Secret's AI capabilities into your own applications and services.

## Overview

The Secret AI SDK is a Python library that enables access to Secret Confidential AI models. The SDK provides a simple and intuitive API that allows you to send requests to Secret's AI models and receive responses in a variety of formats.

## Features

- Access to Secret Confidential AI models
- Simple and intuitive API

## Requirements

`secret-ai-sdk` has a list of dependencies as defined in the `requirements.txt` file. All, except `secret-sdk-python`, are listed in the `pyproject.toml` file.

You will need to install `secret-sdk-python` as shown below:

```bash
pip install 'secret-sdk>=1.8.1'
```

## Installation

To install the Secret AI SDK, you can use pip:

```bash
pip install secret-ai-sdk
```

## Usage

Here's an example of how to use the Secret AI SDK:

```python
from secret_ai_sdk.secret_ai import ChatSecret
from secret_ai_sdk.secret import Secret

secret_client = Secret()
# Get all the models registered with the smart contracts
models = secret_client.get_models()
# For the chosen model, you may obtain a list of LLM instance URLs to connect to
urls = secret_client.get_urls(model=models[0])
# You previously exported the env var SECRET_AI_API_KEY=YOUR-API-KEY
secret_ai_llm = ChatSecret(
    base_url=urls[0],  # in this case, we choose to access the first URL in the list
    model=models[0],  # your previously selected model
    temperature=1.0
)
# Define your messages to send to the confidential LLM for processing
messages = [
    ("system", "You are a helpful assistant that translates English to French. Translate the user sentence."),
    ("human", "I love programming."),
]
# Invoke the LLM
response = secret_ai_llm.invoke(messages, stream=False)
print(response.content)
```

If you do not need to select a specific LLM URL (let's say your agent does not need to worry about the contextual memory from previous sessions), you can make a simplified call to `ChatSecret`. Given the exported env var `SECRET_AI_API_KEY='YOUR_API_KEY'`:

```python
from secret_ai_sdk.secret_ai import ChatSecret

model = ChatSecret(model='llama3.1:70b')

response = model.invoke([system_message, human_message])

print(response)
```

You can reference `test_secret_ai.py` and `test_secret.py` to see how we tested the code, as it may help you in writing your own implementation.

## Manually Setting Up `node_url`

If you experience issues with the default `node_url` (`SECRET_NODE_URL_DEFAULT` config variable), instead of declaring the client like this:

```python
secret_client = Secret()
```

you can manually specify a `node_url` when instantiating the `Secret` client:

```python
from secret_ai_sdk.secret import Secret

secret_client = Secret(chain_id='pulsar-3', node_url=<LCD_NODE_URL>)
```

Alternatively, you can set the `node_url` via an environment variable:

```bash
export SECRET_NODE_URL=<LCD_NODE_URL>
```

For more details on available endpoints and a list of LCD nodes, refer to the official Secret Network documentation:
[Connecting to the Network - Testnet Pulsar-3](https://docs.scrt.network/secret-network-documentation/development/resources-api-contract-addresses/connecting-to-the-network/testnet-pulsar-3)

## API Documentation

For more information on the Secret AI SDK API, please see our [API documentation](https://docs.scrt.network/secret-network-documentation/secret-ai/sdk).

## License

The Secret AI SDK is licensed under the [MIT License](https://opensource.org/licenses/MIT).

