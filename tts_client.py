#!/usr/bin/env python3
"""
SecretAI TTS Service Testing Script - Aligned with OpenAI Compatible Endpoints
Tests the actual Kokoro TTS endpoints based on the router implementation
"""

import requests
import json
import base64
import time
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
import argparse
import os

API_KEY = os.getenv('SECRET_AI_API_KEY')

class SecretAITTSTester:
    def __init__(self, host: str = "localhost", port: int = 25435):
        self.base_url = f"https://{host}:{port}"
        self.session = requests.Session()
        
        # Set common headers based on actual implementation
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if API_KEY:
            self.session.headers['Authorization'] = f'Basic {API_KEY}'
    
    def check_health(self) -> bool:
        """Check if SecretAI TTS service is healthy"""
        print("🏥 Checking SecretAI TTS Service Health...")
        
        try:
            # Test the models endpoint (actual endpoint from router)
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                models = response.json()
                print("✅ Service is healthy (models endpoint accessible)")
                print(f"  Available models: {[m['id'] for m in models.get('data', [])]}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def get_available_models(self) -> Optional[List[Dict]]:
        """Get available models using the actual /models endpoint"""
        print("🤖 Getting Available Models...")
        
        try:
            response = self.session.get(f"{self.base_url}/v1/models", timeout=10)
            if response.status_code == 200:
                models_data = response.json()
                models = models_data.get('data', [])
                print("✅ Available models:")
                for model in models:
                    print(f"  - {model['id']} (owned by: {model.get('owned_by', 'unknown')})")
                return models
            else:
                print(f"❌ Failed to get models: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"❌ Error getting models: {e}")
            return None
    
    def get_specific_model(self, model_id: str) -> Optional[Dict]:
        """Get specific model info using /models/{model} endpoint"""
        print(f"🔍 Getting model info for: {model_id}")
        
        try:
            response = self.session.get(f"{self.base_url}/v1/models/{model_id}", timeout=10)
            if response.status_code == 200:
                model_info = response.json()
                print(f"✅ Model {model_id} details:")
                for key, value in model_info.items():
                    print(f"  {key}: {value}")
                return model_info
            elif response.status_code == 404:
                print(f"❌ Model {model_id} not found")
                return None
            else:
                print(f"❌ Failed to get model {model_id}: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"❌ Error getting model {model_id}: {e}")
            return None
    
    def get_available_voices(self) -> Optional[List[str]]:
        """Get available voices using the actual /audio/voices endpoint"""
        print("🎭 Getting Available Voices...")
        
        try:
            response = self.session.get(f"{self.base_url}/v1/audio/voices", timeout=10)
            if response.status_code == 200:
                voices_data = response.json()
                voices = voices_data.get('voices', [])
                print("✅ Available voices:")
                for voice in sorted(voices):
                    print(f"  - {voice}")
                return voices
            else:
                print(f"❌ Failed to get voices: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"❌ Error getting voices: {e}")
            return None
    
    def test_openai_speech_endpoint(self, text: str = "Hello, this is a test of the OpenAI compatible text to speech API.") -> bool:
        """Test the main OpenAI-compatible /audio/speech endpoint"""
        print(f"🗣️ Testing OpenAI Speech Endpoint with text: '{text[:50]}...'")
        
        # Test different configurations based on the OpenAISpeechRequest schema
        test_configs = [
            {
                "model": "tts-1",
                "input": text,
                "voice": "alloy"  # OpenAI standard voice
            },
            {
                "model": "tts-1-hd", 
                "input": text,
                "voice": "echo",
                "response_format": "mp3"
            },
            {
                "model": "kokoro",
                "input": text, 
                "voice": "af_heart",  # Kokoro voice
                "response_format": "wav",
                "speed": 1.0
            },
            {
                "model": "tts-1",
                "input": text,
                "voice": "af_nova",
                "response_format": "opus",
                "speed": 1.2
            }
        ]
        
        success_count = 0
        for i, config in enumerate(test_configs):
            print(f"  Testing config {i+1}: {config['model']} with voice {config['voice']}")
            
            try:
                response = self.session.post(
                    f"{self.base_url}/v1/audio/speech",
                    json=config,
                    timeout=60
                )
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    content_length = len(response.content)
                    
                    print(f"    ✅ Success! Content-Type: {content_type}, Size: {content_length} bytes")
                    
                    # Save audio if requested
                    if "--save-audio" in sys.argv:
                        format_ext = config.get('response_format', 'wav')
                        self._save_raw_audio(
                            response.content, 
                            f"openai_speech_test_{i}_{config['voice']}",
                            format_ext
                        )
                    
                    success_count += 1
                    
                elif response.status_code == 400:
                    try:
                        error = response.json()
                        print(f"    ❌ Validation error: {error.get('detail', {}).get('message', 'Unknown error')}")
                    except:
                        print(f"    ❌ Bad request: {response.status_code}")
                else:
                    print(f"    ❌ Failed with status: {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"    ❌ Request error: {e}")
        
        print(f"✅ OpenAI Speech endpoint test completed: {success_count}/{len(test_configs)} configs successful")
        return success_count > 0
    
    def test_streaming_speech(self, text: str = "This is a test of streaming audio generation.") -> bool:
        """Test streaming audio generation"""
        print(f"🌊 Testing Streaming Speech with text: '{text[:50]}...'")
        
        streaming_config = {
            "model": "tts-1",
            "input": text,
            "voice": "alloy",
            "response_format": "mp3",
            "stream": True  # Enable streaming
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/audio/speech",
                json=streaming_config,
                timeout=60,
                stream=True  # Enable streaming on client side
            )
            
            if response.status_code == 200:
                print("    ✅ Streaming response received")
                
                # Collect streamed data
                audio_chunks = []
                chunk_count = 0
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        audio_chunks.append(chunk)
                        chunk_count += 1
                
                total_size = sum(len(chunk) for chunk in audio_chunks)
                print(f"    📊 Received {chunk_count} chunks, total size: {total_size} bytes")
                
                # Save complete audio if requested
                if "--save-audio" in sys.argv:
                    complete_audio = b''.join(audio_chunks)
                    self._save_raw_audio(complete_audio, "streaming_test", "mp3")
                
                return True
            else:
                print(f"    ❌ Streaming failed with status: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"    ❌ Streaming error: {e}")
            return False
    
    def test_voice_combinations(self) -> bool:
        """Test voice combination functionality using /audio/voices/combine endpoint"""
        print("🎭 Testing Voice Combinations...")
        
        # First get available voices
        voices = self.get_available_voices()
        if not voices or len(voices) < 2:
            print("    ⚠️ Not enough voices available for combination testing")
            return False
        
        # Test different combination formats
        test_combinations = [
            voices[0] + "+" + voices[1],  # String format
            [voices[0], voices[1]],       # List format
        ]
        
        if len(voices) >= 3:
            test_combinations.append(voices[0] + "+" + voices[1] + "+" + voices[2])
        
        success_count = 0
        for i, combination in enumerate(test_combinations):
            print(f"  Testing combination {i+1}: {combination}")
            
            try:
                response = self.session.post(
                    f"{self.base_url}/v1/audio/voices/combine",
                    json=combination,
                    timeout=30
                )
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    content_length = len(response.content)
                    
                    print(f"    ✅ Success! Content-Type: {content_type}, Size: {content_length} bytes")
                    
                    # Save .pt file if requested
                    if "--save-audio" in sys.argv:
                        combo_name = "+".join(combination) if isinstance(combination, list) else combination.replace("+", "_")
                        self._save_raw_audio(response.content, f"voice_combo_{combo_name}", "pt")
                    
                    success_count += 1
                    
                elif response.status_code == 403:
                    print(f"    ⚠️ Voice combination disabled on server")
                    break
                elif response.status_code == 400:
                    try:
                        error = response.json()
                        print(f"    ❌ Validation error: {error.get('detail', {}).get('message', 'Unknown error')}")
                    except:
                        print(f"    ❌ Bad request: {response.status_code}")
                else:
                    print(f"    ❌ Failed with status: {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"    ❌ Request error: {e}")
        
        print(f"✅ Voice combination test completed: {success_count}/{len(test_combinations)} combinations successful")
        return success_count > 0
    
    def test_advanced_features(self) -> bool:
        """Test advanced features like download links and different formats"""
        print("⚙️ Testing Advanced Features...")
        
        test_text = "Testing advanced TTS features and parameters."
        
        # Test with download link feature
        advanced_configs = [
            {
                "model": "tts-1",
                "input": test_text,
                "voice": "alloy",
                "response_format": "wav",
                "return_download_link": True
            },
            {
                "model": "kokoro", 
                "input": test_text,
                "voice": "af_sky",
                "response_format": "flac",
                "speed": 0.8,
                "volume_multiplier": 1.2
            },
            {
                "model": "tts-1-hd",
                "input": test_text,
                "voice": "shimmer", 
                "response_format": "aac",
                "stream": True,
                "return_download_link": True,
                "download_format": "wav"
            }
        ]
        
        success_count = 0
        for i, config in enumerate(advanced_configs):
            print(f"  Testing advanced config {i+1}: {list(config.keys())}")
            
            try:
                response = self.session.post(
                    f"{self.base_url}/v1/audio/speech",
                    json=config,
                    timeout=60,
                    stream=config.get('stream', False)
                )
                
                if response.status_code == 200:
                    # Check for download link in headers
                    download_path = response.headers.get('X-Download-Path')
                    if download_path:
                        print(f"    ✅ Download link provided: {download_path}")
                    
                    content_length = len(response.content) if not config.get('stream') else "streaming"
                    print(f"    ✅ Success! Content length: {content_length}")
                    
                    # Save audio if requested
                    if "--save-audio" in sys.argv:
                        format_ext = config.get('response_format', 'wav')
                        if config.get('stream'):
                            # Handle streaming response
                            audio_data = b''.join(response.iter_content(chunk_size=8192))
                        else:
                            audio_data = response.content
                        
                        self._save_raw_audio(audio_data, f"advanced_test_{i}", format_ext)
                    
                    success_count += 1
                    
                elif response.status_code == 400:
                    try:
                        error = response.json()
                        print(f"    ❌ Validation error: {error.get('detail', {}).get('message', 'Unknown error')}")
                    except:
                        print(f"    ❌ Bad request: {response.status_code}")
                else:
                    print(f"    ❌ Failed with status: {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"    ❌ Request error: {e}")
        
        print(f"✅ Advanced features test completed: {success_count}/{len(advanced_configs)} configs successful")
        return success_count > 0
    
    def test_download_endpoint(self, filename: str = "test_download.wav") -> bool:
        """Test the download endpoint if available"""
        print(f"📁 Testing Download Endpoint with filename: {filename}")
        
        try:
            response = self.session.get(f"{self.base_url}/v1/download/{filename}", timeout=30)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                content_length = len(response.content)
                print(f"    ✅ Download successful! Content-Type: {content_type}, Size: {content_length} bytes")
                
                if "--save-audio" in sys.argv:
                    self._save_raw_audio(response.content, "downloaded_file", filename.split('.')[-1])
                
                return True
            elif response.status_code == 404:
                print(f"    ℹ️ File {filename} not found (expected for test)")
                return False
            else:
                print(f"    ❌ Download failed with status: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"    ❌ Download error: {e}")
            return False
    
    def _save_raw_audio(self, audio_bytes: bytes, filename_prefix: str, extension: str = "wav"):
        """Save raw audio bytes with proper extension"""
        output_dir = Path("tts_test_outputs")
        output_dir.mkdir(exist_ok=True)
        
        filename = f"{filename_prefix}_{int(time.time())}.{extension}"
        filepath = output_dir / filename
        
        with open(filepath, "wb") as f:
            f.write(audio_bytes)
        
        print(f"    📁 Saved to: {filepath}")
    
