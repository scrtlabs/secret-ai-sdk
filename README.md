# Secret AI SDK

[![PyPI version](https://img.shields.io/pypi/v/secret-ai-sdk.svg)](https://pypi.org/project/secret-ai-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/secret-ai-sdk.svg)](https://pypi.org/project/secret-ai-sdk/)
[![License](https://img.shields.io/github/license/scrtlabs/secret-ai-sdk.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/secret-ai-sdk.svg)](https://pypi.org/project/secret-ai-sdk/)

**The Secret AI SDK provides a comprehensive Python interface for accessing Secret Network's confidential AI models**, offering privacy-preserving artificial intelligence capabilities including text generation, speech processing, and multimodal AI interactions. Built for enterprise-grade reliability with automatic retry logic, comprehensive error handling, and seamless integration patterns.

---

## 🌟 **Why Secret AI SDK?**

✅ **Privacy-First AI**: All computations run in confidential virtual machines  
✅ **Enterprise-Ready**: Built-in retry logic, error handling, and monitoring  
✅ **Multi-Modal**: Support for text, audio, and vision processing  
✅ **Developer-Friendly**: Clean APIs with comprehensive documentation  
✅ **Production-Tested**: Used in production environments with robust reliability

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

## 📦 **Quick Start**

### Installation

Install the Secret AI SDK with pip:

```bash
# Install the latest version
pip install secret-ai-sdk

# Install with development dependencies (optional)
pip install secret-ai-sdk[dev]

# Verify installation
python -c "import secret_ai_sdk; print(f'Secret AI SDK v{secret_ai_sdk.__version__} installed successfully!')"
```

### System Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, Linux  
- **Memory**: Minimum 512MB RAM (2GB recommended for larger models)
- **Network**: Internet connection for API access

### Get Your API Key

1. Visit the [Secret AI Developer Portal](https://aidev.scrtlabs.com/)
2. Sign up for an account or log in
3. Generate your API key
4. Set it as an environment variable:

```bash
# Linux/macOS
export SECRET_AI_API_KEY='your_api_key_here'

# Windows Command Prompt
set SECRET_AI_API_KEY=your_api_key_here

# Windows PowerShell
$env:SECRET_AI_API_KEY='your_api_key_here'

# Or add to your .env file
echo "SECRET_AI_API_KEY=your_api_key_here" >> .env
```

### 30-Second Example

```python
from secret_ai_sdk import ChatSecret, Secret

# Initialize Secret client and get available models
secret_client = Secret()
models = secret_client.get_models()
urls = secret_client.get_urls(model=models[0])

# Create AI client
ai_client = ChatSecret(base_url=urls[0], model=models[0])

# Send a message
messages = [("human", "What makes Secret AI unique?")]
response = ai_client.invoke(messages)
print(response.content)
```

### Verify Your Setup

Test your installation and API key:

```python
from secret_ai_sdk import Secret
from secret_ai_sdk.secret_ai_ex import SecretAIAPIKeyMissingError

try:
    secret_client = Secret()
    models = secret_client.get_models()
    print(f"✅ Connected successfully! Available models: {len(models)}")
except SecretAIAPIKeyMissingError:
    print("❌ API key missing. Please set SECRET_AI_API_KEY")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## 🔧 **Comprehensive Usage Guide**

### 1. Text Generation & Chat

The core functionality for conversational AI and text generation:

#### Basic Chat Example
```python
from secret_ai_sdk import ChatSecret, Secret

# Initialize and get available services
secret_client = Secret()
models = secret_client.get_models()
urls = secret_client.get_urls(model=models[0])

# Create the AI client
ai_client = ChatSecret(
    base_url=urls[0],
    model=models[0],
    temperature=0.7,  # Controls creativity (0.0-2.0)
    max_tokens=1000,  # Maximum response length
)

# Simple conversation
messages = [
    ("system", "You are a helpful AI assistant specialized in Python programming."),
    ("human", "Explain the difference between list and tuple in Python."),
]

response = ai_client.invoke(messages)
print(response.content)
```

#### Streaming Responses
```python
from secret_ai_sdk import ChatSecret, Secret

# Setup client (same as above)
ai_client = ChatSecret(base_url=urls[0], model=models[0])

messages = [("human", "Write a short story about space exploration")]

# Stream the response token by token
print("🤖 AI Response:")
for chunk in ai_client.stream(messages):
    print(chunk.content, end="", flush=True)
print("\n")
```

#### Multi-turn Conversations
```python
from secret_ai_sdk import ChatSecret, Secret

ai_client = ChatSecret(base_url=urls[0], model=models[0])

# Maintain conversation history
conversation_history = [
    ("system", "You are a helpful coding assistant."),
]

# Function to add message and get response
def chat_with_ai(user_message, history):
    history.append(("human", user_message))
    response = ai_client.invoke(history)
    history.append(("assistant", response.content))
    return response.content, history

# Example conversation
response, conversation_history = chat_with_ai(
    "How do I create a virtual environment in Python?", 
    conversation_history
)
print(f"AI: {response}")

response, conversation_history = chat_with_ai(
    "What packages should I install in it?", 
    conversation_history
)
print(f"AI: {response}")
```

#### Custom Streaming Handler
```python
from secret_ai_sdk import ChatSecret, Secret
from langchain.callbacks.base import BaseCallbackHandler

class CustomStreamHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        # Custom processing for each token
        print(f"[Token]: {token}", end="")

ai_client = ChatSecret(
    base_url=urls[0], 
    model=models[0],
    callbacks=[CustomStreamHandler()]
)

messages = [("human", "Count from 1 to 10")]
ai_client.invoke(messages)  # Will use the custom handler
```

### 2. Voice Processing (Speech-to-Text & Text-to-Speech)

Complete voice processing capabilities with STT and TTS:

#### Setup Voice Services
```python
from secret_ai_sdk.voice_secret import VoiceSecret
from secret_ai_sdk.secret import Secret

# Get voice service endpoints from Secret Network
secret_client = Secret()
models = secret_client.get_models()

# Get service URLs (automatically discovered)
stt_url = secret_client.get_urls(model='stt-whisper')
tts_url = secret_client.get_urls(model='tts-kokoro')

# Initialize voice client
voice_client = VoiceSecret(
    stt_url=stt_url,
    tts_url=tts_url,
    api_key="your_api_key"  # Optional if SECRET_AI_API_KEY env var is set
)
```

#### Text-to-Speech (TTS) Examples
```python
from pathlib import Path

# Create output directory
output_dir = Path("audio_output")
output_dir.mkdir(exist_ok=True)

# Basic text-to-speech
text = "Welcome to Secret AI's text-to-speech service!"
audio_data = voice_client.synthesize_speech(
    text=text,
    model="tts-1",
    voice="af_alloy",
    response_format="mp3",
    speed=1.0  # Normal speed
)

# Save the audio file
output_path = output_dir / "welcome.mp3"
voice_client.save_audio(audio_data, output_path)
print(f"✅ Audio saved to: {output_path}")

# Different voices and formats
voices_to_try = ["af_alloy", "af_heart", "af_nova"]
for voice in voices_to_try:
    audio_data = voice_client.synthesize_speech(
        text=f"This is the {voice} voice speaking.",
        model="tts-1",
        voice=voice,
        response_format="wav",  # Different format
        speed=1.2  # Slightly faster
    )
    output_path = output_dir / f"voice_sample_{voice}.wav"
    voice_client.save_audio(audio_data, output_path)
    print(f"✅ Voice sample saved: {output_path}")
```

#### Streaming Text-to-Speech
```python
# For longer texts, use streaming TTS
long_text = """
This is a longer text that demonstrates streaming text-to-speech synthesis.
Streaming is useful for real-time applications where you want to start
playing audio before the entire text is processed.
"""

audio_data = voice_client.synthesize_speech_streaming(
    text=long_text.strip(),
    model="tts-1",
    voice="af_alloy",
    response_format="mp3"
)

output_path = output_dir / "streaming_tts.mp3"
voice_client.save_audio(audio_data, output_path)
print(f"✅ Streaming TTS saved: {output_path}")
```

#### Speech-to-Text (STT) Examples
```python
# First, let's create a test audio file using TTS
test_text = "This is a test audio file for speech recognition."
test_audio = voice_client.synthesize_speech(
    text=test_text,
    model="tts-1",
    voice="af_alloy",
    response_format="wav"
)

test_file = output_dir / "test_audio.wav"
voice_client.save_audio(test_audio, test_file)

# Now transcribe the audio file
transcription = voice_client.transcribe_audio(test_file)
print(f"📝 Original text: {test_text}")
print(f"🎧 Transcribed text: {transcription['text']}")
print(f"🌍 Detected language: {transcription.get('language', 'unknown')}")

# Streaming speech-to-text
streaming_result = voice_client.transcribe_audio_streaming(test_file)
print(f"🔄 Streaming transcription: {streaming_result['text']}")
```

#### Voice Processing with Context Manager
```python
# Recommended: Use context manager for automatic cleanup
with VoiceSecret(stt_url=stt_url, tts_url=tts_url) as voice:
    # Check service health
    try:
        stt_health = voice.check_stt_health()
        tts_health = voice.check_tts_health()
        print(f"✅ STT Health: {stt_health}")
        print(f"✅ TTS Health: {tts_health}")
    except Exception as e:
        print(f"⚠️ Service health check failed: {e}")
    
    # Get available options
    models = voice.get_available_models()
    voices = voice.get_available_voices()
    
    print(f"📋 Available models: {len(models)}")
    print(f"🎭 Available voices: {voices[:5]}...")  # Show first 5
    
    # Process audio
    result = voice.transcribe_audio("path/to/your/audio.wav")
    print(f"📝 Transcription: {result['text']}")
```

#### Complete Voice Workflow Example
```python
def voice_memo_processor(memo_text: str, output_dir: Path):
    """Complete workflow: Text → TTS → STT → Verification"""
    
    output_dir.mkdir(exist_ok=True)
    
    with VoiceSecret(stt_url=stt_url, tts_url=tts_url) as voice:
        # Step 1: Convert text to speech
        print("🎙️ Converting text to speech...")
        audio_data = voice.synthesize_speech(
            text=memo_text,
            model="tts-1",
            voice="af_alloy",
            response_format="wav"
        )
        
        # Step 2: Save audio file
        memo_file = output_dir / "voice_memo.wav"
        voice.save_audio(audio_data, memo_file)
        print(f"💾 Voice memo saved: {memo_file}")
        
        # Step 3: Transcribe back to text
        print("🎧 Transcribing audio...")
        transcription = voice.transcribe_audio(memo_file)
        
        # Step 4: Save transcription
        transcript_file = output_dir / "transcript.txt"
        with open(transcript_file, 'w') as f:
            f.write(f"Original: {memo_text}\n\n")
            f.write(f"Transcribed: {transcription['text']}\n\n")
            f.write(f"Language: {transcription.get('language', 'unknown')}\n")
        
        print(f"📄 Transcript saved: {transcript_file}")
        return transcription

# Example usage
memo = "Meeting notes: Discuss the new AI features, review budget allocation, and schedule follow-up for next week."
result = voice_memo_processor(memo, Path("voice_workflow_output"))
```

### 3. Enhanced Client with Automatic Retry & Error Handling

The Enhanced Client provides enterprise-grade reliability:

#### Basic Enhanced Client Setup
```python
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient

# Create enhanced client with automatic retry and error handling
client = EnhancedSecretAIClient(
    host="https://your-ai-endpoint.com",
    api_key="your_api_key",  # Optional if env var is set
    timeout=30.0,            # Request timeout in seconds
    max_retries=3,           # Maximum retry attempts
    retry_delay=1.0,         # Initial delay between retries
    retry_backoff=2.0,       # Backoff multiplier for retries
    validate_responses=True  # Validate API responses
)

# The client automatically handles:
# - Network failures with exponential backoff
# - Timeout errors with retry logic
# - Response validation and error recovery
```

#### Production Configuration Example
```python
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient
from secret_ai_sdk.secret_ai_ex import (
    SecretAITimeoutError, 
    SecretAIConnectionError,
    SecretAIRetryExhaustedError
)

# Production-ready configuration
production_client = EnhancedSecretAIClient(
    host="https://ai.secret.network",
    timeout=45.0,          # Longer timeout for production
    connect_timeout=10.0,  # Connection timeout
    max_retries=5,         # More retries for reliability
    retry_delay=2.0,       # Start with 2-second delay
    retry_backoff=1.5,     # Conservative backoff
    validate_responses=True
)

# Robust error handling
def safe_ai_call(prompt: str, max_attempts: int = 3):
    """Make AI call with comprehensive error handling"""
    
    for attempt in range(max_attempts):
        try:
            response = production_client.chat(
                model="your-model",
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
            
        except SecretAITimeoutError as e:
            print(f"⏱️ Timeout on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                raise
                
        except SecretAIConnectionError as e:
            print(f"🔌 Connection error on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                raise
                
        except SecretAIRetryExhaustedError as e:
            print(f"🔄 All retries exhausted: {e}")
            raise
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise

# Example usage
try:
    result = safe_ai_call("Explain quantum computing in simple terms")
    print(f"✅ Success: {result}")
except Exception as e:
    print(f"❌ Final failure: {e}")
```

### 4. Vision & Multimodal Processing

Process images alongside text for comprehensive AI analysis:

#### Basic Image Processing
```python
from secret_ai_sdk import ChatSecret, Secret

# Setup client for vision model
secret_client = Secret()
vision_models = [m for m in secret_client.get_models() if 'vision' in m]
vision_url = secret_client.get_urls(model=vision_models[0])

vision_client = ChatSecret(
    base_url=vision_url[0],
    model=vision_models[0],
    temperature=0.3  # Lower temperature for analytical tasks
)

# Analyze an image
messages = [
    ("human", [
        {"type": "text", "text": "What do you see in this image? Provide a detailed description."},
        {"type": "image_url", "image_url": {"url": "path/to/your/image.jpg"}}
    ])
]

response = vision_client.invoke(messages)
print(f"🖼️ Image Analysis: {response.content}")
```

#### Advanced Vision Tasks
```python
# Multiple images comparison
messages = [
    ("human", [
        {"type": "text", "text": "Compare these two images and identify the key differences:"},
        {"type": "image_url", "image_url": {"url": "image1.jpg"}},
        {"type": "image_url", "image_url": {"url": "image2.jpg"}}
    ])
]

response = vision_client.invoke(messages)
print(f"🔍 Comparison: {response.content}")

# Document analysis
messages = [
    ("human", [
        {"type": "text", "text": "Extract the text from this document and summarize the key points:"},
        {"type": "image_url", "image_url": {"url": "document.png"}}
    ])
]

response = vision_client.invoke(messages)
print(f"📄 Document Analysis: {response.content}")

# Chart/Graph analysis
messages = [
    ("human", [
        {"type": "text", "text": "Analyze this chart and explain the trends you observe:"},
        {"type": "image_url", "image_url": {"url": "chart.png"}}
    ])
]

response = vision_client.invoke(messages)
print(f"📊 Chart Analysis: {response.content}")
```

## ⚙️ **Configuration & Settings**

### API Authentication

#### Getting Your API Key
1. **Register**: Visit the [Secret AI Developer Portal](https://aidev.scrtlabs.com/)
2. **Create Account**: Sign up or log in to your existing account
3. **Generate Key**: Navigate to API Keys section and create a new key
4. **Secure Storage**: Store your key securely and never commit it to code

#### Setting Up Authentication
```bash
# Method 1: Environment Variable (Recommended)
export SECRET_AI_API_KEY='your_api_key_here'

# Method 2: .env File
echo "SECRET_AI_API_KEY=your_api_key_here" >> .env

# Method 3: Shell Profile (Persistent)
echo 'export SECRET_AI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### Programmatic API Key Management
```python
import os
from secret_ai_sdk import ChatSecret

# Method 1: Environment variable (recommended)
client = ChatSecret(base_url=url, model=model)  # Uses SECRET_AI_API_KEY

# Method 2: Direct parameter (use with caution)
client = ChatSecret(
    base_url=url,
    model=model,
    client_kwargs={'api_key': 'your_api_key'}
)

# Method 3: Dynamic loading
api_key = os.getenv('SECRET_AI_API_KEY') or input("Enter API key: ")
client = ChatSecret(
    base_url=url,
    model=model,
    client_kwargs={'api_key': api_key}
)
```

### Environment Variables Reference

Complete list of supported environment variables:

```bash
# Core Authentication
SECRET_AI_API_KEY='your_api_key'              # Required: Your API key

# Network Configuration  
SECRET_NODE_URL='https://lcd.secret.express'  # Optional: Custom LCD node URL
SECRET_AI_REQUEST_TIMEOUT='30.0'             # Optional: Request timeout (seconds)
SECRET_AI_CONNECT_TIMEOUT='10.0'             # Optional: Connection timeout (seconds)

# Retry & Resilience Settings
SECRET_AI_MAX_RETRIES='3'                    # Optional: Maximum retry attempts
SECRET_AI_RETRY_DELAY='1.0'                  # Optional: Initial retry delay (seconds)
SECRET_AI_RETRY_BACKOFF='2.0'                # Optional: Backoff multiplier
SECRET_AI_MAX_RETRY_DELAY='60.0'             # Optional: Maximum retry delay (seconds)

# Logging & Debug
SECRET_AI_LOG_LEVEL='INFO'                   # Optional: Logging level (DEBUG, INFO, WARNING, ERROR)
SECRET_AI_DEBUG='false'                      # Optional: Enable debug mode

# Voice Services (Optional - auto-discovered if not set)
SECRET_AI_STT_URL='https://stt.secret.ai'    # Optional: Speech-to-Text service URL
SECRET_AI_TTS_URL='https://tts.secret.ai'    # Optional: Text-to-Speech service URL
```

### Advanced Configuration

#### Custom Network Configuration
```python
from secret_ai_sdk.secret import Secret

# Custom node configuration
custom_secret_client = Secret(
    chain_id='secret-4',  # Mainnet
    node_url='https://lcd.secret.express'  # Custom LCD endpoint
)

# Testnet configuration
testnet_secret_client = Secret(
    chain_id='pulsar-3',  # Testnet
    node_url='https://lcd.testnet.scrt.network'
)

# Local development
local_secret_client = Secret(
    chain_id='localsecret',
    node_url='http://localhost:1317'
)
```

#### Production Configuration Template
```python
import os
from secret_ai_sdk import ChatSecret, Secret
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient

# Production environment setup
class SecretAIConfig:
    def __init__(self):
        # Required settings
        self.api_key = os.getenv('SECRET_AI_API_KEY')
        if not self.api_key:
            raise ValueError("SECRET_AI_API_KEY environment variable is required")
        
        # Network settings
        self.node_url = os.getenv('SECRET_NODE_URL', 'https://lcd.secret.express')
        self.request_timeout = float(os.getenv('SECRET_AI_REQUEST_TIMEOUT', '45.0'))
        self.connect_timeout = float(os.getenv('SECRET_AI_CONNECT_TIMEOUT', '10.0'))
        
        # Retry settings
        self.max_retries = int(os.getenv('SECRET_AI_MAX_RETRIES', '5'))
        self.retry_delay = float(os.getenv('SECRET_AI_RETRY_DELAY', '2.0'))
        self.retry_backoff = float(os.getenv('SECRET_AI_RETRY_BACKOFF', '1.5'))
        
        # Service discovery
        self.secret_client = Secret(node_url=self.node_url)
        self.available_models = self.secret_client.get_models()
        
    def create_chat_client(self, model_name: str = None):
        """Create a production-ready chat client"""
        model = model_name or self.available_models[0]
        urls = self.secret_client.get_urls(model=model)
        
        return ChatSecret(
            base_url=urls[0],
            model=model,
            temperature=0.7,
            client_kwargs={
                'api_key': self.api_key,
                'timeout': self.request_timeout,
                'max_retries': self.max_retries,
                'retry_delay': self.retry_delay,
                'retry_backoff': self.retry_backoff
            }
        )

# Usage
config = SecretAIConfig()
chat_client = config.create_chat_client()
```

### Configuration Validation

```python
from secret_ai_sdk import Secret
from secret_ai_sdk.secret_ai_ex import *

def validate_configuration():
    """Validate Secret AI SDK configuration"""
    issues = []
    
    # Check API key
    import os
    api_key = os.getenv('SECRET_AI_API_KEY')
    if not api_key:
        issues.append("❌ SECRET_AI_API_KEY not set")
    elif len(api_key) < 10:
        issues.append("⚠️ API key seems too short")
    else:
        issues.append("✅ API key configured")
    
    # Test network connectivity
    try:
        secret_client = Secret()
        models = secret_client.get_models()
        issues.append(f"✅ Network connectivity OK ({len(models)} models available)")
    except Exception as e:
        issues.append(f"❌ Network connectivity failed: {e}")
    
    # Check service availability
    try:
        if models:
            urls = secret_client.get_urls(model=models[0])
            if urls:
                issues.append("✅ Service discovery working")
            else:
                issues.append("⚠️ No service URLs found")
    except Exception as e:
        issues.append(f"⚠️ Service discovery issues: {e}")
    
    return issues

# Run validation
print("🔍 Secret AI SDK Configuration Check:")
for issue in validate_configuration():
    print(f"  {issue}")
```

## 🔧 **Advanced Features & Error Handling**

### Exception Handling

The SDK provides comprehensive error handling with specific exception types:

```python
from secret_ai_sdk.secret_ai_ex import (
    SecretAIAPIKeyMissingError,
    SecretAIConnectionError, 
    SecretAITimeoutError,
    SecretAIRetryExhaustedError,
    SecretAIResponseError,
    SecretAINetworkError
)

def robust_ai_interaction(prompt: str):
    """Example of comprehensive error handling"""
    try:
        # Your AI interaction code
        secret_client = Secret()
        models = secret_client.get_models()
        urls = secret_client.get_urls(model=models[0])
        
        ai_client = ChatSecret(base_url=urls[0], model=models[0])
        response = ai_client.invoke([("human", prompt)])
        return response.content
        
    except SecretAIAPIKeyMissingError:
        print("❌ API key missing. Set SECRET_AI_API_KEY environment variable")
        return None
        
    except SecretAITimeoutError as e:
        print(f"⏱️ Request timed out after {e.timeout} seconds")
        return None
        
    except SecretAIConnectionError as e:
        print(f"🔌 Connection failed to {e.host}: {e.original_error}")
        return None
        
    except SecretAIRetryExhaustedError as e:
        print(f"🔄 All {e.attempts} retry attempts failed: {e.last_error}")
        return None
        
    except SecretAIResponseError as e:
        print(f"📝 Invalid response format: {e}")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

# Usage
result = robust_ai_interaction("Explain machine learning")
if result:
    print(f"✅ Success: {result}")
```

## 🚀 **Performance & Best Practices**

### Performance Optimization

#### Connection Pooling & Reuse
```python
from secret_ai_sdk import ChatSecret, Secret

# ✅ Good: Reuse clients for multiple requests
class AIService:
    def __init__(self):
        secret_client = Secret()
        models = secret_client.get_models()
        urls = secret_client.get_urls(model=models[0])
        
        # Create client once, reuse many times
        self.client = ChatSecret(
            base_url=urls[0],
            model=models[0],
            temperature=0.7
        )
    
    def generate_response(self, prompt: str):
        return self.client.invoke([("human", prompt)])

# ❌ Bad: Creating new client for each request
def bad_example(prompt: str):
    secret_client = Secret()
    models = secret_client.get_models()
    urls = secret_client.get_urls(model=models[0])
    client = ChatSecret(base_url=urls[0], model=models[0])
    return client.invoke([("human", prompt)])
```

#### Optimal Timeout Settings
```python
# Different timeout strategies for different use cases

# Real-time applications (chatbots, interactive tools)
realtime_client = ChatSecret(
    base_url=url,
    model=model,
    client_kwargs={
        'timeout': 15.0,        # Quick responses
        'connect_timeout': 5.0,
        'max_retries': 2
    }
)

# Batch processing (data analysis, content generation)
batch_client = ChatSecret(
    base_url=url,
    model=model,
    client_kwargs={
        'timeout': 120.0,       # Allow longer processing
        'connect_timeout': 15.0,
        'max_retries': 5
    }
)

# Critical applications (production services)
production_client = ChatSecret(
    base_url=url,
    model=model,
    client_kwargs={
        'timeout': 60.0,
        'connect_timeout': 10.0,
        'max_retries': 3,
        'retry_delay': 2.0,
        'retry_backoff': 1.5
    }
)
```

#### Memory Management
```python
import gc
from secret_ai_sdk.voice_secret import VoiceSecret

# For large file processing
def process_large_audio_files(file_paths: list):
    """Handle large audio files efficiently"""
    
    with VoiceSecret() as voice:
        results = []
        
        for i, file_path in enumerate(file_paths):
            try:
                # Process file
                result = voice.transcribe_audio(file_path)
                results.append(result)
                
                # Periodic garbage collection for large batches
                if i % 10 == 0:
                    gc.collect()
                    
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                continue
        
        return results
```

### Best Practices Checklist

#### ✅ **Security Best Practices**
```python
import os
from secret_ai_sdk import ChatSecret

# ✅ Use environment variables for API keys
api_key = os.getenv('SECRET_AI_API_KEY')
if not api_key:
    raise ValueError("API key not configured")

# ✅ Validate inputs before sending to AI
def sanitize_input(user_input: str) -> str:
    """Basic input sanitization"""
    if len(user_input) > 10000:
        raise ValueError("Input too long")
    if not user_input.strip():
        raise ValueError("Empty input")
    return user_input.strip()

# ✅ Handle sensitive data appropriately
def process_sensitive_prompt(prompt: str):
    """Example: Handle sensitive data"""
    try:
        sanitized = sanitize_input(prompt)
        # Process with AI...
        response = client.invoke([("human", sanitized)])
        return response.content
    except Exception as e:
        # Log error without exposing sensitive data
        print(f"Processing failed: {type(e).__name__}")
        return None
```

#### ✅ **Resource Management**
```python
# ✅ Always use context managers for voice processing
with VoiceSecret() as voice:
    result = voice.transcribe_audio("file.wav")

# ✅ Implement proper cleanup in classes
class AIAssistant:
    def __init__(self):
        self.client = ChatSecret(base_url=url, model=model)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup resources if needed
        if hasattr(self.client, 'close'):
            self.client.close()
```

#### ✅ **Error Resilience**
```python
import time
import random
from secret_ai_sdk.secret_ai_ex import SecretAINetworkError

def resilient_ai_call(prompt: str, max_retries: int = 3):
    """Implement custom retry with exponential backoff"""
    
    for attempt in range(max_retries):
        try:
            response = client.invoke([("human", prompt)])
            return response.content
            
        except SecretAINetworkError as e:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff with jitter
            delay = (2 ** attempt) + random.uniform(0, 1)
            print(f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s")
            time.sleep(delay)
```

## 🔍 **Troubleshooting Guide**

### Common Issues & Solutions

#### **1. API Key Issues**

**Problem**: `SecretAIAPIKeyMissingError`
```python
# ❌ Error: Missing API key
SecretAIAPIKeyMissingError: Missing API Key. Environment variable SECRET_AI_API_KEY must be set
```

**Solutions**:
```bash
# Check if API key is set
echo $SECRET_AI_API_KEY

# Set API key (choose one method)
export SECRET_AI_API_KEY='your_actual_api_key'
echo "SECRET_AI_API_KEY=your_actual_api_key" >> .env

# Verify in Python
python -c "import os; print('API Key:', os.getenv('SECRET_AI_API_KEY', 'NOT SET'))"
```

#### **2. Network Connectivity Issues**

**Problem**: `SecretAIConnectionError`
```python
# ❌ Error: Cannot connect to services
SecretAIConnectionError: Failed to connect to https://ai.secret.network
```

**Diagnostic Steps**:
```python
import requests
from secret_ai_sdk import Secret

# Test 1: Check internet connectivity
try:
    response = requests.get('https://google.com', timeout=5)
    print("✅ Internet connectivity: OK")
except:
    print("❌ No internet connection")

# Test 2: Check Secret Network connectivity  
try:
    secret_client = Secret()
    models = secret_client.get_models()
    print(f"✅ Secret Network: OK ({len(models)} models)")
except Exception as e:
    print(f"❌ Secret Network issue: {e}")

# Test 3: Check specific service endpoints
try:
    urls = secret_client.get_urls(model=models[0])
    response = requests.get(f"{urls[0]}/api/tags", timeout=10)
    print("✅ AI service: OK")
except Exception as e:
    print(f"❌ AI service issue: {e}")
```

**Solutions**:
```python
# Try different network configuration
from secret_ai_sdk.secret import Secret

# Option 1: Use different LCD node
secret_client = Secret(node_url='https://lcd.secret.express')

# Option 2: Use testnet
secret_client = Secret(
    chain_id='pulsar-3',
    node_url='https://lcd.testnet.scrt.network'
)

# Option 3: Configure custom timeouts
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient
client = EnhancedSecretAIClient(
    host=urls[0],
    timeout=60.0,
    connect_timeout=15.0
)
```

#### **3. Voice Service Issues**

**Problem**: Voice services not available
```python
# ❌ Error: Voice services not responding
VoiceServiceError: STT service health check failed
```

**Diagnostic & Solutions**:
```python
from secret_ai_sdk.voice_secret import VoiceSecret
from secret_ai_sdk.secret import Secret

# Diagnostic
def diagnose_voice_services():
    try:
        secret_client = Secret()
        models = secret_client.get_models()
        
        # Check if voice models are available
        voice_models = [m for m in models if 'stt' in m or 'tts' in m]
        print(f"Available voice models: {voice_models}")
        
        if not voice_models:
            print("❌ No voice models found")
            return
        
        # Test voice service URLs
        stt_url = secret_client.get_urls(model='stt-whisper')
        tts_url = secret_client.get_urls(model='tts-kokoro')
        
        print(f"STT URL: {stt_url}")
        print(f"TTS URL: {tts_url}")
        
        # Test individual services
        with VoiceSecret(stt_url=stt_url, tts_url=tts_url) as voice:
            try:
                voice.check_stt_health()
                print("✅ STT service: OK")
            except Exception as e:
                print(f"❌ STT service: {e}")
            
            try:
                voice.check_tts_health()
                print("✅ TTS service: OK")
            except Exception as e:
                print(f"❌ TTS service: {e}")
                
    except Exception as e:
        print(f"❌ Voice service diagnosis failed: {e}")

diagnose_voice_services()
```

#### **4. Performance Issues**

**Problem**: Slow responses or timeouts
```python
# Symptoms: Requests taking too long or timing out
SecretAITimeoutError: request timed out after 30.0 seconds
```

**Solutions**:
```python
import time
from secret_ai_sdk import ChatSecret

# Solution 1: Optimize request parameters
fast_client = ChatSecret(
    base_url=url,
    model=model,
    max_tokens=500,        # Limit response length
    temperature=0.3,       # Lower temperature = faster
    client_kwargs={
        'timeout': 45.0,   # Increase timeout
        'max_retries': 2   # Reduce retries for speed
    }
)

# Solution 2: Use streaming for long responses
def fast_streaming_response(prompt: str):
    start_time = time.time()
    response_chunks = []
    
    for chunk in fast_client.stream([("human", prompt)]):
        response_chunks.append(chunk.content)
        # Process chunks as they arrive
        print(chunk.content, end="", flush=True)
    
    total_time = time.time() - start_time
    print(f"\nResponse completed in {total_time:.2f} seconds")
    return "".join(response_chunks)

# Solution 3: Batch similar requests
def batch_process_prompts(prompts: list):
    """Process multiple prompts efficiently"""
    results = []
    
    for i, prompt in enumerate(prompts):
        try:
            response = fast_client.invoke([("human", prompt)])
            results.append(response.content)
            
            # Add small delay to avoid overwhelming the service
            if i < len(prompts) - 1:
                time.sleep(0.5)
                
        except Exception as e:
            print(f"Failed prompt {i}: {e}")
            results.append(None)
    
    return results
```

### **Debug Mode & Logging**

```python
import logging
from secret_ai_sdk import ChatSecret

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('secret_ai_sdk')

# Set environment variable for debug mode
import os
os.environ['SECRET_AI_DEBUG'] = 'true'
os.environ['SECRET_AI_LOG_LEVEL'] = 'DEBUG'

# This will now show detailed request/response information
client = ChatSecret(base_url=url, model=model)
response = client.invoke([("human", "test message")])
```

### **Getting Help**

If you're still experiencing issues:

1. **Check Service Status**: Visit [Secret AI Status Page](https://status.scrt.network)
2. **Review Logs**: Enable debug logging to see detailed error information
3. **Test Configuration**: Run the configuration validation script
4. **Community Support**: Join the [Secret Network Discord](https://discord.gg/secret-network)
5. **Report Issues**: [GitHub Issues](https://github.com/scrtlabs/secret-ai-sdk/issues)

```python
# Quick diagnostic script
def run_diagnostics():
    """Run comprehensive diagnostics"""
    print("🔍 Running Secret AI SDK Diagnostics...")
    
    # Include all the validation functions from above
    validate_configuration()
    diagnose_voice_services()
    
    print("\n📋 Diagnostic Summary:")
    print("If issues persist, include this output when reporting bugs.")

if __name__ == "__main__":
    run_diagnostics()
```

## 📚 **Additional Resources**

### **Example Files**
- `example.py` - Comprehensive text generation examples
- `voice_example.py` - Voice processing workflows  
- `example_vision.py` - Vision and multimodal examples

### **API Documentation**
- [Official Documentation](https://docs.scrt.network/secret-network-documentation/secret-ai/sdk)
- [Secret Network Docs](https://docs.scrt.network/)
- [Developer Portal](https://aidev.scrtlabs.com/)

### **Community & Support**
- [GitHub Repository](https://github.com/scrtlabs/secret-ai-sdk)
- [Discord Community](https://discord.gg/secret-network)
- [Secret Network Website](https://scrt.network)

---

## 📄 **License**

The Secret AI SDK is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## 🤝 **Contributing**

We welcome contributions! Please read our contributing guidelines and feel free to submit pull requests.

## 🆘 **Support**

If you encounter issues or have questions:
1. Check this README and troubleshooting guide
2. Search [existing issues](https://github.com/scrtlabs/secret-ai-sdk/issues)
3. Create a [new issue](https://github.com/scrtlabs/secret-ai-sdk/issues/new) with details

---

*Built with ❤️ by the Secret Network community*
