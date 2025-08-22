# voice_secret.py

"""
Module: VoiceSecret provides STT and TTS functionality through SecretAI SDK
"""

import os
import requests
from typing import Optional, Dict, Any, List, Union, BinaryIO
from pathlib import Path
import logging

import secret_ai_sdk._config as _config
from secret_ai_sdk.secret_ai_ex import SecretAIAPIKeyMissingError

logger = logging.getLogger(__name__)

class VoiceSecret:
    """
    VoiceSecret provides Speech-to-Text and Text-to-Speech functionality
    through the SecretAI platform endpoints.
    
    This class combines STT and TTS capabilities in a unified interface,
    supporting both HTTP and WebSocket protocols for various use cases.
    """
    
    def __init__(self, 
                 stt_url: str = "https://localhost:25436", 
                 tts_url: str = "https://localhost:25435", 
                 api_key: Optional[str] = None):
        """
        Initialize VoiceSecret client.
        
        Args:
            stt_host: STT service hostname
            stt_port: STT service port
            tts_host: TTS service hostname  
            tts_port: TTS service port
            api_key: Secret AI API Key. If None, reads from SECRET_AI_API_KEY env var
        """
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)
        
        if not api_key:
            raise SecretAIAPIKeyMissingError()
            
        self.api_key = api_key
        
        # STT configuration
        self.stt_http_url = stt_url
        
        # TTS configuration
        self.tts_base_url = tts_url
        
        # Setup HTTP session for TTS
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Basic {self.api_key}'
        })
    
    # STT Methods
    
    def transcribe_audio(self, audio_file: Union[str, Path, BinaryIO]) -> Dict[str, Any]:
        """
        Transcribe audio file using HTTP STT endpoint.
        
        Args:
            audio_file: Path to audio file or file-like object
            
        Returns:
            Dictionary containing transcription results with keys:
            - text: The transcribed text
            - language: Detected language (if available)
            
        Raises:
            requests.RequestException: If the request fails
        """
        headers = {'Authorization': f'Basic {self.api_key}'}
        
        if isinstance(audio_file, (str, Path)):
            with open(audio_file, 'rb') as f:
                files = {'audio': f}
                response = requests.post(f"{self.stt_http_url}/stt", files=files, headers=headers)
        else:
            files = {'audio': audio_file}
            response = requests.post(f"{self.stt_http_url}/stt", files=files, headers=headers)
        
        response.raise_for_status()
        return response.json()
    
    def transcribe_audio_streaming(self, audio_file: Union[str, Path, BinaryIO]) -> Dict[str, Any]:
        """
        Transcribe audio file using HTTP streaming STT endpoint.
        
        Args:
            audio_file: Path to audio file or file-like object
            
        Returns:
            Dictionary containing streaming transcription results with keys:
            - text: Full transcribed text
            - chunks_processed: Number of chunks processed
            - partial_results: List of partial transcription results
            
        Raises:
            requests.RequestException: If the request fails
        """
        headers = {'Authorization': f'Basic {self.api_key}'}
        
        if isinstance(audio_file, (str, Path)):
            with open(audio_file, 'rb') as f:
                files = {'audio': f}
                response = requests.post(f"{self.stt_http_url}/stt_stream", files=files, headers=headers, stream=True)
        else:
            files = {'audio': audio_file}
            response = requests.post(f"{self.stt_http_url}/stt_stream", files=files, headers=headers, stream=True)
        
        response.raise_for_status()
        return response.json()
    
    
    def check_stt_health(self) -> Dict[str, Any]:
        """
        Check STT service health.
        
        Returns:
            Dictionary containing health status information
        """
        headers = {'Authorization': f'Basic {self.api_key}'}
        response = requests.get(f"{self.stt_http_url}/healthz", headers=headers)
        response.raise_for_status()
        return response.json()
    
    # TTS Methods
    
    def synthesize_speech(self, 
                         text: str,
                         model: str = "tts-1",
                         voice: str = "af_alloy",
                         response_format: str = "mp3",
                         speed: float = 1.0,
                         **kwargs) -> bytes:
        """
        Synthesize speech from text using OpenAI-compatible endpoint.
        
        Args:
            text: Text to synthesize
            model: TTS model to use (e.g., "tts-1", "tts-1-hd", "kokoro")
            voice: Voice to use (e.g., "alloy", "echo", "af_heart")
            response_format: Audio format ("mp3", "wav", "opus", "aac", "flac")
            speed: Speech speed (0.25 to 4.0)
            **kwargs: Additional parameters like volume_multiplier, return_download_link
            
        Returns:
            Audio data as bytes
            
        Raises:
            requests.RequestException: If the request fails
        """
        config = {
            "model": model,
            "input": text,
            "voice": voice,
            "response_format": response_format,
            "speed": speed,
            **kwargs
        }
        
        response = self.session.post(
            f"{self.tts_base_url}/v1/audio/speech",
            json=config,
            timeout=60
        )
        
        response.raise_for_status()
        return response.content
    
    def synthesize_speech_streaming(self,
                                  text: str,
                                  model: str = "tts-1", 
                                  voice: str = "af_alloy",
                                  response_format: str = "mp3",
                                  speed: float = 1.0,
                                  **kwargs) -> bytes:
        """
        Synthesize speech with streaming response.
        
        Args:
            text: Text to synthesize
            model: TTS model to use
            voice: Voice to use
            response_format: Audio format
            speed: Speech speed
            **kwargs: Additional parameters
            
        Returns:
            Complete audio data as bytes
        """
        config = {
            "model": model,
            "input": text,
            "voice": voice,
            "response_format": response_format,
            "speed": speed,
            "stream": True,
            **kwargs
        }
        
        response = self.session.post(
            f"{self.tts_base_url}/v1/audio/speech",
            json=config,
            timeout=60,
            stream=True
        )
        
        response.raise_for_status()
        
        # Collect streamed chunks
        audio_chunks = []
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                audio_chunks.append(chunk)
        
        return b''.join(audio_chunks)
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available TTS models.
        
        Returns:
            List of model dictionaries with id, owned_by, etc.
        """
        response = self.session.get(f"{self.tts_base_url}/v1/models", timeout=10)
        response.raise_for_status()
        models_data = response.json()
        return models_data.get('data', [])
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific model.
        
        Args:
            model_id: ID of the model to query
            
        Returns:
            Model information dictionary or None if not found
        """
        response = self.session.get(f"{self.tts_base_url}/v1/models/{model_id}", timeout=10)
        
        if response.status_code == 404:
            return None
            
        response.raise_for_status()
        return response.json()
    
    def get_available_voices(self) -> List[str]:
        """
        Get list of available voices.
        
        Returns:
            List of voice names
        """
        response = self.session.get(f"{self.tts_base_url}/v1/audio/voices", timeout=10)
        response.raise_for_status()
        voices_data = response.json()
        return voices_data.get('voices', [])
    
    def combine_voices(self, voices: Union[str, List[str]]) -> bytes:
        """
        Combine multiple voices into a single voice model.
        
        Args:
            voices: Voice names to combine (string with '+' separator or list)
            
        Returns:
            Combined voice model data as bytes
        """
        response = self.session.post(
            f"{self.tts_base_url}/v1/audio/voices/combine",
            json=voices,
            timeout=30
        )
        
        response.raise_for_status()
        return response.content
    
    def download_file(self, filename: str) -> bytes:
        """
        Download a file from the TTS service.
        
        Args:
            filename: Name of the file to download
            
        Returns:
            File content as bytes
        """
        response = self.session.get(f"{self.tts_base_url}/v1/download/{filename}", timeout=30)
        response.raise_for_status()
        return response.content
    
    def check_tts_health(self) -> Dict[str, Any]:
        """
        Check TTS service health.
        
        Returns:
            Dictionary containing health status information
        """
        response = self.session.get(f"{self.tts_base_url}/health", timeout=10)
        response.raise_for_status()
        return response.json()
    
    # Utility Methods
    
    def save_audio(self, audio_data: bytes, filepath: Union[str, Path], format_hint: str = "wav"):
        """
        Save audio data to file.
        
        Args:
            audio_data: Audio data as bytes
            filepath: Path to save the file
            format_hint: File format hint for extension
        """
        filepath = Path(filepath)
        if not filepath.suffix:
            filepath = filepath.with_suffix(f".{format_hint}")
        
        # Create directory if it doesn't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        
        logger.info(f"Audio saved to: {filepath}")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, *_):
        """Context manager exit."""
        self.close()