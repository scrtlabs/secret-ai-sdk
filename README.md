# Claive AI SDK
The Claive AI SDK provides a simple and convenient way to access Claive Confidential AI models. With this SDK, you can easily integrate Claive's AI capabilities into your own applications and services.

## Overview
The Claive AI SDK is a Python library that enables access to Claive Confidential AI models. The SDK provides a simple and intuitive API that allows you to send requests to Claive's AI models and receive responses in a variety of formats.

## Features
* Access to Claive Confidential AI models
* Simple and intuitive API

## Requirements
claive-sdk has a list of dependencies as defined in requirements.txt file
All, but secret-sdk-python, are listed in pyproject.toml file 

You will need to install secret-sdk-python as shown below:
```bash
pip install git+https://github.com/scrtlabs/secret-sdk-python.git@main
```

## Installation
To install the Claive AI SDK, you can use pip:
```bash
pip install git+https://github.com/scrtlabs/claive-sdk.git
```
## Usage
Here's an example of how to use the Claive AI SDK:
```python
from claive_sdk.claive import ChatClaive
from claive_sdk.secret import SecretClaive


secret_client = SecretClaive()
# Get all the models registered with the smart contracts
models = secret_client.get_models()
# For the chosen model you may obtain a list of LLM instance URLs to connect to
urls = secret_client.get_urls(model=models[0])
# You previosly exported the env var CLAIVE_AI_API_KEY=YOUR-API-KEY
claive_llm = ChatClaive(
base_url=urls[0], # in this case we choose to access the first url in the list
model=model, # your previosly selected model
temperature=1.
)
# Define your messages you want to send to the confidential LLM for processing
messages = [
(
      "system",
      "You are a helpful assistant that translates English to French. Translate the user sentence.",
),
("human", "I love programming."),
]
# Invoke the llm
response = claive_llm.invoke(messages, stream=False)
print(response.content)
```

If you do not need to select a specific LLM URL (let's say your agent does not need to worry about the contextual memory from previous sessions), you can make a simplified call to ChatClaive. Given the exported env var CLAIVE_AI_API_KEY='YOUR_API_KEY':

```python
from claive_sdk.claive import ChatClaive

model = ChatClaive(model='llama3.1:70b')

response = model.invoke([system_message, human_message])

print(response)
```

You can reference test_claive.py and test_secret.py to see how we tested the code as it may help you in writing your own implementation.

## API Documentation
For more information on the Claive AI SDK API, please see our [API documentation](https://claive.ai/docs/api).

## Contributing
We welcome contributions to the Claive AI SDK. If you're interested in contributing, please see our [contributing guidelines](https://claive.ai/docs/contributing).

## License
The Claive AI SDK is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Support
If you have any questions or need help with the Claive AI SDK, please don't hesitate to contact us:
* Email: [support@claive.ai](mailto:support@claive.ai)
* GitHub: [https://github.com/claive/claive-ai-sdk](https://github.com/claive/claive-ai-sdk)

