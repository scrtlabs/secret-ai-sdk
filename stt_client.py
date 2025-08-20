#!/usr/bin/env python3
"""
Example client for the STT streaming service
"""

import asyncio
import websockets
import json
import numpy as np
# import sounddevice as sd
import requests
from typing import Optional
import os
import io
from pydub import AudioSegment
from pydub.playback import play
import time

API_KEY = os.getenv('SECRET_AI_API_KEY')

class STTStreamingClient:
    def __init__(self, host: str = "localhost", port: int = 25434):
        self.host = host
        self.port = port
        self.ws_url = f"wss://{host}:{port}/ws/stt_stream"
        self.http_url = f"https://{host}:{port}"
        
    
    async def _listen_for_transcripts(self, websocket):
        """Listen for transcription results from WebSocket"""
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data.get("type") == "partial_transcript":
                    print(f"📝 Partial: {data['text']}")
                elif data.get("type") == "final_transcript":
                    print(f"✅ Final: {data['text']}")
                elif data.get("type") == "stream_ended":
                    print("🏁 Stream ended")
                    break
                elif data.get("type") == "error":
                    print(f"❌ Error: {data['error']}")
                    break
                else:
                    print(f"ℹ️ Info: {data}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("🔌 WebSocket connection closed")
        except Exception as e:
            print(f"❌ Listen error: {e}")
    
    def test_http_stt(self, audio_file: str):
        """Test standard HTTP STT endpoint"""
        print(f"📄 Testing HTTP STT with file: {audio_file}")
        
        try:
            headers = {}
            if API_KEY:
                headers['Authorization'] = f'Basic {API_KEY}'
            
            with open(audio_file, 'rb') as f:
                files = {'audio': f}
                response = requests.post(f"{self.http_url}/stt", files=files, headers=headers)
                
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Transcription: {result['text']}")
                print(f"🌐 Language: {result.get('language', 'unknown')}")
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ HTTP STT error: {e}")
    
    def test_http_streaming_stt(self, audio_file: str):
        """Test HTTP streaming STT endpoint"""
        print(f"📄 Testing HTTP streaming STT with file: {audio_file}")
        
        try:
            headers = {}
            if API_KEY:
                headers['Authorization'] = f'Basic {API_KEY}'
            
            with open(audio_file, 'rb') as f:
                files = {'audio': f}
                response = requests.post(f"{self.http_url}/stt_stream", files=files, headers=headers, stream=True)
                
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Full transcription: {result['text']}")
                print(f"📊 Chunks processed: {result['chunks_processed']}")
                
                for i, partial in enumerate(result['partial_results']):
                    final_marker = " (FINAL)" if partial.get('final') else ""
                    print(f"  Chunk {i}: {partial['text']}{final_marker}")
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ HTTP streaming STT error: {e}")
    
    def check_health(self):
        """Check service health"""
        try:
            headers = {}
            if API_KEY:
                headers['Authorization'] = f'Basic {API_KEY}'
            
            response = requests.get(f"{self.http_url}/healthz", headers=headers)
            if response.status_code == 200:
                health = response.json()
                print("🟢 Service is healthy:")
                for key, value in health.items():
                    print(f"  {key}: {value}")
            else:
                print(f"🔴 Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
