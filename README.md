# Secret AI SDK

[![PyPI version](https://img.shields.io/pypi/v/secret-ai-sdk.svg)](https://pypi.org/project/secret-ai-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/secret-ai-sdk.svg)](https://pypi.org/project/secret-ai-sdk/)
[![License](https://img.shields.io/github/license/scrtlabs/secret-ai-sdk.svg)](https://opensource.org/licenses/MIT)

The Secret AI SDK provides a comprehensive Python interface for accessing Secret Network's confidential AI models, including text generation, speech-to-text (STT), and text-to-speech (TTS) capabilities. Built with enterprise-grade reliability and privacy-preserving features.

## Overview

The Secret AI SDK is a Python library that enables secure, private access to Secret Network's confidential AI infrastructure. The SDK provides intuitive APIs for text-based language models, voice processing, and multimodal AI capabilities while ensuring all computations remain confidential through Secret's privacy-preserving technology.

## Features

### Core AI Capabilities
- **Text Generation**: Access to Secret Confidential AI language models with streaming support
- **Voice Processing**: Unified STT and TTS functionality through the VoiceSecret class
- **Multimodal Support**: Handle text, audio, and voice interactions seamlessly

### Enterprise-Grade Reliability
- **Enhanced Error Handling**: Comprehensive exception hierarchy with detailed error context
- **Automatic Retry Logic**: Configurable exponential backoff for network resilience
- **Timeout Management**: Customizable request and connection timeout controls
- **Response Validation**: Built-in validation for API response integrity

### Developer Experience
- **Clean Pythonic Interface**: Intuitive APIs following Python best practices
- **Flexible Authentication**: API key-based authentication with environment variable support
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Context Manager Support**: Proper resource management with context managers

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

### Text Generation

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

### Voice Processing with VoiceSecret

```python
from secret_ai_sdk.voice_secret import VoiceSecret
from secret_ai_sdk.secret import Secret

# First, query smart contract to get available models and service URLs
secret_client = Secret()
models = secret_client.get_models()

# Check if required models are available
if 'stt-whisper' not in models:
    raise ValueError("STT Whisper model not available")
if 'tts-kokoro' not in models:
    raise ValueError("TTS Kokoro model not available")

# Get service URLs from smart contract for each model
stt_url = secret_client.get_urls(model='stt-whisper')
if stt_url is None:
    raise ValueError("STT url not available")
tts_url = secret_client.get_urls(model='tts-kokoro')
if tts_url is None:
    raise ValueError("TTS url not available")

# Initialize VoiceSecret client with smart contract URLs
voice_client = VoiceSecret(
    stt_url=stt_url,
    tts_url=tts_url,
    api_key="your_api_key"  # Optional, reads from SECRET_AI_API_KEY env var
)

# Speech-to-Text: Transcribe audio file
transcription = voice_client.transcribe_audio("path/to/audio.wav")
print(f"Transcribed text: {transcription['text']}")

# Text-to-Speech: Generate speech from text
audio_data = voice_client.synthesize_speech(
    text="Hello, this is a test of the Secret AI TTS system.",
    model="tts-1",
    voice="af_alloy",
    response_format="mp3"
)

# Save the generated audio
voice_client.save_audio(audio_data, "output/speech.mp3")

# Use as context manager for automatic cleanup
with VoiceSecret() as voice:
    # Get available voices and models
    voices = voice.get_available_voices()
    models = voice.get_available_models()
    
    # Health checks
    stt_health = voice.check_stt_health()
    tts_health = voice.check_tts_health()
```

### Enhanced Client with Retry Logic

```python
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient

# Create enhanced client with automatic retry and error handling
client = EnhancedSecretAIClient(
    host="https://your-ai-endpoint.com",
    api_key="your_api_key",
    timeout=30.0,
    max_retries=3,
    retry_delay=1.0,
    retry_backoff=2.0
)

# Generate with automatic retry on failures
response = client.generate(
    model="your-model",
    prompt="Write a short story about AI.",
    stream=False
)
```

## Configuration

### API Key Authentication

To use the Secret AI SDK, you need your own Secret AI API Key. Visit SecreAI Development portal: [https://aidev.scrtlabs.com/](https://aidev.scrtlabs.com/).

Set your API key as an environment variable:

```bash
export SECRET_AI_API_KEY='YOUR_API_KEY'
```

### Environment Variables

The SDK supports various environment variables for configuration:

```bash
# Authentication
export SECRET_AI_API_KEY='your_api_key'

# Network Configuration
export SECRET_NODE_URL='your_lcd_node_url'

# Timeout Settings (seconds)
export SECRET_AI_REQUEST_TIMEOUT='30.0'
export SECRET_AI_CONNECT_TIMEOUT='10.0'

# Retry Configuration
export SECRET_AI_MAX_RETRIES='3'
export SECRET_AI_RETRY_DELAY='1.0'
export SECRET_AI_RETRY_BACKOFF='2.0'
export SECRET_AI_MAX_RETRY_DELAY='60.0'
```

### Node URL Configuration

If you experience issues with the default node URL, you can manually specify one:

```python
from secret_ai_sdk.secret import Secret

# Option 1: Directly in code
secret_client = Secret(chain_id='secret-4', node_url='YOUR_LCD_NODE_URL')

# Option 2: Using an environment variable
# export SECRET_NODE_URL='YOUR_LCD_NODE_URL'
```

For available endpoints and LCD nodes, see the [Secret Network Documentation](https://docs.scrt.network/secret-network-documentation/development/resources-api-contract-addresses/connecting-to-the-network/testnet-pulsar-3).

## Advanced Features

### Error Handling

The SDK provides comprehensive error handling with specific exception types:

```python
from secret_ai_sdk.secret_ai_ex import (
    SecretAIAPIKeyMissingError,
    SecretAIConnectionError, 
    SecretAITimeoutError,
    SecretAIRetryExhaustedError,
    SecretAIResponseError
)

try:
    response = client.generate(model="test", prompt="Hello")
except SecretAITimeoutError as e:
    print(f"Request timed out after {e.timeout} seconds")
except SecretAIConnectionError as e:
    print(f"Failed to connect to {e.host}: {e.original_error}")
except SecretAIRetryExhaustedError as e:
    print(f"All {e.attempts} retry attempts failed: {e.last_error}")
```

### Streaming Responses

Both text generation and TTS support streaming for real-time processing:

```python
# Streaming text generation
for chunk in secret_ai_llm.stream(messages):
    print(chunk.content, end="", flush=True)

# Streaming TTS
audio_data = voice_client.synthesize_speech_streaming(
    text="Long text to be synthesized...",
    model="tts-1"
)
```

### Custom Retry Configuration

Configure retry behavior per client instance:

```python
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient

client = EnhancedSecretAIClient(
    host="https://ai-endpoint.com",
    max_retries=5,           # Retry up to 5 times
    retry_delay=2.0,         # Start with 2 second delay
    retry_backoff=1.5,       # Increase delay by 1.5x each retry
    timeout=45.0,            # 45 second request timeout
    validate_responses=True   # Validate response format
)
```

## Examples

For comprehensive examples including streaming implementation, refer to the `example.py` and `voice_example.py` files provided in the package.

## API Documentation

For comprehensive API documentation, please visit our [official documentation](https://docs.scrt.network/secret-network-documentation/secret-ai/sdk).

## License

The Secret AI SDK is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/scrtlabs/secret-ai-sdk/issues) on our GitHub repository.
