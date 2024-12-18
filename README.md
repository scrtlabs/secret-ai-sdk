# Claive AI SDK
The Claive AI SDK provides a simple and convenient way to access Claive Confidential AI models. With this SDK, you can easily integrate Claive's AI capabilities into your own applications and services.

## Overview
The Claive AI SDK is a Python library that enables access to Claive Confidential AI models. The SDK provides a simple and intuitive API that allows you to send requests to Claive's AI models and receive responses in a variety of formats.

## Features
* Access to Claive Confidential AI models
* Simple and intuitive API

## Installation
To install the Claive AI SDK, you can use pip:
```bash
pip install claive-sdk-python
```
## Usage
Here's an example of how to use the Claive AI SDK:
```python
from claive_sdk.claive import ChatClaive
from claive_sdk.registry import RegistryClaive

llm_model = 'llama3.1:70b'

models = RegistryClaive.get_models()

if llm_model in models:
      urls = RegistryClaive.get_urls(model)
      model = ChatClaive(
            base_url=urls[0],
            model=llm_model,
            temperature=llm_temperature,
            api_key="YOUR_API_KEY"
      )

response = model.invoke([system_message, summary_message, human_message])

print(response)
```

If you do not need to select a specific LLM URL (let's say your agent does not need to worry about the contextual memory from previous sessions), you can make a simplified call to ChatClaive. Given the exported env var CLAIVE_AI_API_KEY='YOUR_API_KEY':

```python
from claive_sdk.claive import ChatClaive

model = ChatClaive(model='llama3.1:70b')

response = model.invoke([system_message, human_message])

print(response)
```

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

