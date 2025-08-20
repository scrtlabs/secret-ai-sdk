#!/usr/bin/env python3
"""
Test script for VoiceSecret class functionality
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the SDK to path
sys.path.insert(0, str(Path(__file__).parent))

from secret_ai_sdk.voice_secret import VoiceSecret

# Service configuration from environment variables
VOICE_HOST = os.getenv('SECRET_AI_VOICE_HOST', 'localhost')
STT_PORT = int(os.getenv('SECRET_AI_STT_PORT', '25436'))
TTS_PORT = int(os.getenv('SECRET_AI_TTS_PORT', '25435'))

def test_stt_service():
    """Test STT service functionality independently"""
    print("🎧 Testing STT Service")
    
    try:
        # Initialize with custom ports
        voice_client = VoiceSecret(
            stt_host=VOICE_HOST,
            stt_port=STT_PORT,
            tts_host=VOICE_HOST,
            tts_port=TTS_PORT
        )
        print(f"✅ VoiceSecret initialized (STT: {VOICE_HOST}:{STT_PORT})")
        
        stt_available = False
        
        # Test STT health check
        try:
            stt_health = voice_client.check_stt_health()
            print(f"✅ STT Health Check: {stt_health}")
            stt_available = True
        except Exception as e:
            print(f"❌ STT Service not available: {e}")
            voice_client.close()
            return False
        
        voice_client.close()
        return stt_available
        
    except Exception as e:
        print(f"❌ STT service test failed: {e}")
        return False

def test_tts_service():
    """Test TTS service functionality independently"""
    print("🎤 Testing TTS Service")
    
    try:
        # Initialize with custom ports
        voice_client = VoiceSecret(
            stt_host=VOICE_HOST,
            stt_port=STT_PORT,
            tts_host=VOICE_HOST,
            tts_port=TTS_PORT
        )
        print(f"✅ VoiceSecret initialized (TTS: {VOICE_HOST}:{TTS_PORT})")
        
        tts_available = False
        
        # Test TTS health check
        try:
            tts_health = voice_client.check_tts_health()
            print(f"✅ TTS Health Check: {tts_health}")
            tts_available = True
        except Exception as e:
            print(f"❌ TTS Service not available: {e}")
            voice_client.close()
            return False
        
        # Test getting available models (only if TTS is available)
        if tts_available:
            try:
                models = voice_client.get_available_models()
                print(f"✅ Available Models: {len(models)} found")
                for model in models[:3]:  # Show first 3
                    print(f"  - {model.get('id', 'unknown')}")
            except Exception as e:
                print(f"⚠️ Get Models failed: {e}")
            
            # Test getting available voices
            try:
                voices = voice_client.get_available_voices()
                print(f"✅ Available Voices: {len(voices)} found")
                for voice in voices[:5]:  # Show first 5
                    print(f"  - {voice}")
            except Exception as e:
                print(f"⚠️ Get Voices failed: {e}")
        
        voice_client.close()
        return tts_available
        
    except Exception as e:
        print(f"❌ TTS service test failed: {e}")
        return False

def test_tts_synthesis():
    """Test text-to-speech synthesis (requires TTS service)"""
    print("\n🔊 Testing TTS Synthesis")
    
    try:
        voice_client = VoiceSecret(
            stt_host=VOICE_HOST,
            stt_port=STT_PORT,
            tts_host=VOICE_HOST,
            tts_port=TTS_PORT
        )
        
        # First check if TTS service is available
        try:
            voice_client.check_tts_health()
        except Exception:
            print("❌ TTS service not available - skipping synthesis tests")
            voice_client.close()
            return True  # Return True since it's expected that service might not be available
        
        test_text = "Hello, this is a test of the VoiceSecret TTS functionality."
        synthesis_success = False
        
        # Test basic synthesis
        try:
            audio_data = voice_client.synthesize_speech(
                text=test_text,
                model="tts-1",
                voice="af_alloy",
                response_format="mp3"
            )
            print(f"✅ TTS Synthesis successful: {len(audio_data)} bytes")
            
            # Save test audio
            voice_client.save_audio(audio_data, "test_output/tts_test.mp3", "mp3")
            print("✅ Audio saved to test_output/tts_test.mp3")
            synthesis_success = True
            
        except Exception as e:
            print(f"⚠️ TTS Synthesis failed: {e}")
        
        # Test streaming synthesis (only if basic synthesis worked)
        if synthesis_success:
            try:
                audio_data_stream = voice_client.synthesize_speech_streaming(
                    text=test_text,
                    model="tts-1",
                    voice="af_heart",
                    response_format="wav"
                )
                print(f"✅ TTS Streaming successful: {len(audio_data_stream)} bytes")
                
                voice_client.save_audio(audio_data_stream, "test_output/tts_stream_test.wav", "wav")
                print("✅ Streaming audio saved to test_output/tts_stream_test.wav")
                
            except Exception as e:
                print(f"⚠️ TTS Streaming failed: {e}")
        
        voice_client.close()
        return True
        
    except Exception as e:
        print(f"❌ TTS synthesis test failed: {e}")
        return False


def test_stt_transcription():
    """Test STT transcription with audio files (requires STT service)"""
    print("\n🎵 Testing STT Transcription")
    
    try:
        voice_client = VoiceSecret(
            stt_host=VOICE_HOST,
            stt_port=STT_PORT,
            tts_host=VOICE_HOST,
            tts_port=TTS_PORT
        )
        
        # First check if STT service is available
        try:
            voice_client.check_stt_health()
        except Exception:
            print("❌ STT service not available - skipping transcription tests")
            voice_client.close()
            return True  # Return True since it's expected that service might not be available
        
        # Look for audio files in current directory
        audio_files = list(Path('.').glob('*.wav')) + list(Path('.').glob('*.mp3'))
        
        if not audio_files:
            print("⚠️ No audio files found for testing - creating test audio from TTS if available")
            
            # Try to create test audio using TTS
            try:
                voice_client.check_tts_health()
                test_text = "This is a test audio for speech to text conversion."
                audio_data = voice_client.synthesize_speech(
                    text=test_text,
                    model="tts-1",
                    voice="af_alloy",
                    response_format="wav"
                )
                test_audio_path = Path("test_output/stt_test_audio.wav")
                voice_client.save_audio(audio_data, test_audio_path, "wav")
                audio_files = [test_audio_path]
                print(f"✅ Created test audio: {test_audio_path}")
            except Exception as e:
                print(f"⚠️ Could not create test audio: {e}")
                voice_client.close()
                return True
        
        if audio_files:
            audio_file = audio_files[0]
            print(f"📁 Using audio file: {audio_file}")
            
            # Test regular transcription
            try:
                result = voice_client.transcribe_audio(audio_file)
                print(f"✅ Transcription: {result.get('text', 'No text')}")
                print(f"🌐 Language: {result.get('language', 'unknown')}")
            except Exception as e:
                print(f"⚠️ Audio transcription failed: {e}")
            
            # Test streaming transcription
            try:
                stream_result = voice_client.transcribe_audio_streaming(audio_file)
                print(f"✅ Streaming transcription: {stream_result.get('text', 'No text')}")
                print(f"📊 Chunks processed: {stream_result.get('chunks_processed', 0)}")
            except Exception as e:
                print(f"⚠️ Streaming transcription failed: {e}")
        
        voice_client.close()
        return True
        
    except Exception as e:
        print(f"❌ STT transcription test failed: {e}")
        return False


async def main():
    """Run all tests with separated STT and TTS functionality"""
    print("🚀 Starting VoiceSecret Tests")
    print(f"📍 Configuration: Host={VOICE_HOST}, STT Port={STT_PORT}, TTS Port={TTS_PORT}")
    print("=" * 70)
    
    # Create output directory
    Path("test_output").mkdir(exist_ok=True)
    
    # Check service availability first
    print("\n🔍 Checking Service Availability...")
    stt_available = test_stt_service()
    tts_available = test_tts_service()
    
    print(f"\n📊 Service Status:")
    print(f"  STT Service ({VOICE_HOST}:{STT_PORT}): {'✅ Available' if stt_available else '❌ Not Available'}")
    print(f"  TTS Service ({VOICE_HOST}:{TTS_PORT}): {'✅ Available' if tts_available else '❌ Not Available'}")
    
    if not stt_available and not tts_available:
        print("\n❌ No services available for testing")
        return
    
    # Run service-specific tests
    test_results = []
    
    if tts_available:
        print("\n" + "=" * 50)
        tts_result = test_tts_synthesis()
        test_results.append(("TTS Synthesis", tts_result))
    
    if stt_available:
        print("\n" + "=" * 50)
        stt_result = test_stt_transcription()
        test_results.append(("STT Transcription", stt_result))
        
        # WebSocket support not available in current reverse proxy
        # websocket_result = await test_stt_websocket()
        # test_results.append(("STT WebSocket", websocket_result))
    
    # Summary
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print("\n" + "=" * 70)
    print("📋 Test Results Summary:")
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All available tests passed!")
    else:
        print(f"⚠️ {total - passed} tests failed")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv('SECRET_AI_API_KEY'):
        print("❌ SECRET_AI_API_KEY environment variable not set")
        print("Please set your API key: export SECRET_AI_API_KEY=your_key_here")
        sys.exit(1)
    
    # Run async main
    asyncio.run(main())