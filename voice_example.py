#!/usr/bin/env python3
"""
Voice Example: Comprehensive demonstration of Secret AI SDK Voice capabilities

This example showcases the VoiceSecret class functionality including:
- Text-to-Speech (TTS) synthesis with various models and voices
- Speech-to-Text (STT) transcription capabilities  
- Service health monitoring and error handling
- Practical usage patterns and best practices

Requirements:
- SECRET_AI_API_KEY environment variable set
- Access to Secret AI Voice services (STT/TTS endpoints)

Usage:
    python voice_example.py
    
Environment Variables:
    SECRET_AI_API_KEY: Your Secret AI API key (required)
    SECRET_AI_VOICE_HOST: Voice service hostname (default: localhost)
    SECRET_AI_STT_PORT: STT service port (default: 25436)
    SECRET_AI_TTS_PORT: TTS service port (default: 25435)
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional

# Import the Secret AI SDK
from secret_ai_sdk.voice_secret import VoiceSecret
from secret_ai_sdk.secret_ai_ex import (
    SecretAIAPIKeyMissingError,
    SecretAIConnectionError,
    SecretAITimeoutError,
    SecretAIResponseError
)

# Configuration from environment variables
VOICE_HOST = os.getenv('SECRET_AI_VOICE_HOST', 'localhost')
STT_PORT = int(os.getenv('SECRET_AI_STT_PORT', '25436'))
TTS_PORT = int(os.getenv('SECRET_AI_TTS_PORT', '25435'))

def print_header(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step: str):
    """Print a formatted step"""
    print(f"\n📌 {step}")

def print_success(message: str):
    """Print a success message"""
    print(f"✅ {message}")

def print_warning(message: str):
    """Print a warning message"""
    print(f"⚠️  {message}")

def print_error(message: str):
    """Print an error message"""
    print(f"❌ {message}")

def example_basic_setup():
    """Example 1: Basic VoiceSecret setup and initialization"""
    print_header("Example 1: Basic Setup and Initialization")
    
    try:
        # Initialize VoiceSecret with default configuration
        voice_client = VoiceSecret()
        print_success("VoiceSecret initialized with default settings")
        
        # Initialize with custom configuration
        voice_client_custom = VoiceSecret(
            stt_host=VOICE_HOST,
            stt_port=STT_PORT,
            tts_host=VOICE_HOST,
            tts_port=TTS_PORT,
            api_key=os.getenv('SECRET_AI_API_KEY')
        )
        print_success(f"VoiceSecret initialized with custom settings:")
        print(f"  - STT Endpoint: {VOICE_HOST}:{STT_PORT}")
        print(f"  - TTS Endpoint: {VOICE_HOST}:{TTS_PORT}")
        
        # Clean up
        voice_client.close()
        voice_client_custom.close()
        
        return True
        
    except SecretAIAPIKeyMissingError:
        print_error("API key missing. Please set SECRET_AI_API_KEY environment variable")
        return False
    except Exception as e:
        print_error(f"Setup failed: {e}")
        return False

def example_service_health_checks():
    """Example 2: Service health monitoring and availability checks"""
    print_header("Example 2: Service Health Monitoring")
    
    try:
        with VoiceSecret(stt_host=VOICE_HOST, stt_port=STT_PORT, 
                        tts_host=VOICE_HOST, tts_port=TTS_PORT) as voice:
            
            print_step("Checking STT service health...")
            try:
                stt_health = voice.check_stt_health()
                print_success(f"STT Service: {stt_health}")
            except Exception as e:
                print_warning(f"STT service unavailable: {e}")
            
            print_step("Checking TTS service health...")
            try:
                tts_health = voice.check_tts_health()
                print_success(f"TTS Service: {tts_health}")
            except Exception as e:
                print_warning(f"TTS service unavailable: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def example_tts_capabilities():
    """Example 3: Text-to-Speech capabilities and options"""
    print_header("Example 3: Text-to-Speech (TTS) Capabilities")
    
    try:
        with VoiceSecret(stt_host=VOICE_HOST, stt_port=STT_PORT,
                        tts_host=VOICE_HOST, tts_port=TTS_PORT) as voice:
            
            # Check TTS availability first
            try:
                voice.check_tts_health()
            except Exception:
                print_warning("TTS service not available - skipping TTS examples")
                return True
            
            print_step("Getting available models and voices...")
            try:
                models = voice.get_available_models()
                print_success(f"Available models: {len(models)}")
                for model in models[:3]:  # Show first 3
                    print(f"  - {model.get('id', 'unknown')}")
                
                voices = voice.get_available_voices()
                print_success(f"Available voices: {len(voices)}")
                for voice_name in voices[:5]:  # Show first 5
                    print(f"  - {voice_name}")
            except Exception as e:
                print_warning(f"Could not fetch models/voices: {e}")
            
            # Create output directory
            output_dir = Path("voice_examples_output")
            output_dir.mkdir(exist_ok=True)
            
            print_step("Synthesizing speech with different configurations...")
            
            # Example 1: Basic TTS
            try:
                text = "Hello! This is a demonstration of Secret AI's text-to-speech capabilities."
                audio_data = voice.synthesize_speech(
                    text=text,
                    model="tts-1",
                    voice="af_alloy",
                    response_format="mp3"
                )
                output_path = output_dir / "basic_tts.mp3"
                voice.save_audio(audio_data, output_path)
                print_success(f"Basic TTS saved: {output_path} ({len(audio_data)} bytes)")
            except Exception as e:
                print_warning(f"Basic TTS failed: {e}")
            
            # Example 2: Different voice and format
            try:
                text = "This is the same text but with a different voice and audio format."
                audio_data = voice.synthesize_speech(
                    text=text,
                    model="tts-1",
                    voice="af_heart", 
                    response_format="wav",
                    speed=1.2
                )
                output_path = output_dir / "different_voice.wav"
                voice.save_audio(audio_data, output_path)
                print_success(f"Different voice TTS saved: {output_path} ({len(audio_data)} bytes)")
            except Exception as e:
                print_warning(f"Different voice TTS failed: {e}")
            
            # Example 3: Streaming TTS
            try:
                text = "This is a longer text that demonstrates streaming text-to-speech synthesis, which can be useful for real-time applications."
                audio_data = voice.synthesize_speech_streaming(
                    text=text,
                    model="tts-1",
                    voice="af_alloy",
                    response_format="mp3"
                )
                output_path = output_dir / "streaming_tts.mp3"
                voice.save_audio(audio_data, output_path)
                print_success(f"Streaming TTS saved: {output_path} ({len(audio_data)} bytes)")
            except Exception as e:
                print_warning(f"Streaming TTS failed: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"TTS examples failed: {e}")
        return False

def example_stt_capabilities():
    """Example 4: Speech-to-Text capabilities and transcription"""
    print_header("Example 4: Speech-to-Text (STT) Capabilities")
    
    try:
        with VoiceSecret(stt_host=VOICE_HOST, stt_port=STT_PORT,
                        tts_host=VOICE_HOST, tts_port=TTS_PORT) as voice:
            
            # Check STT availability first
            try:
                voice.check_stt_health()
            except Exception:
                print_warning("STT service not available - skipping STT examples")
                return True
            
            output_dir = Path("voice_examples_output")
            output_dir.mkdir(exist_ok=True)
            
            print_step("Creating test audio for transcription...")
            
            # First, create test audio using TTS (if available)
            test_audio_path = None
            try:
                voice.check_tts_health()
                test_text = "This is a test audio file created for speech-to-text transcription demonstration."
                audio_data = voice.synthesize_speech(
                    text=test_text,
                    model="tts-1",
                    voice="af_alloy",
                    response_format="wav"
                )
                test_audio_path = output_dir / "test_for_stt.wav"
                voice.save_audio(audio_data, test_audio_path)
                print_success(f"Test audio created: {test_audio_path}")
                print(f"Original text: '{test_text}'")
            except Exception as e:
                print_warning(f"Could not create test audio with TTS: {e}")
                
                # Look for existing audio files
                audio_files = list(Path('.').glob('*.wav')) + list(Path('.').glob('*.mp3'))
                if audio_files:
                    test_audio_path = audio_files[0]
                    print_success(f"Using existing audio file: {test_audio_path}")
                else:
                    print_warning("No audio files available for STT testing")
                    return True
            
            if test_audio_path and test_audio_path.exists():
                print_step("Transcribing audio...")
                
                # Example 1: Basic transcription
                try:
                    result = voice.transcribe_audio(test_audio_path)
                    print_success("Basic transcription:")
                    print(f"  Text: '{result.get('text', 'No text')}'")
                    print(f"  Language: {result.get('language', 'unknown')}")
                except Exception as e:
                    print_warning(f"Basic transcription failed: {e}")
                
                # Example 2: Streaming transcription
                try:
                    stream_result = voice.transcribe_audio_streaming(test_audio_path)
                    print_success("Streaming transcription:")
                    print(f"  Text: '{stream_result.get('text', 'No text')}'")
                    print(f"  Chunks processed: {stream_result.get('chunks_processed', 0)}")
                    if 'partial_results' in stream_result:
                        print(f"  Partial results: {len(stream_result['partial_results'])}")
                except Exception as e:
                    print_warning(f"Streaming transcription failed: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"STT examples failed: {e}")
        return False

def example_error_handling():
    """Example 5: Error handling and best practices"""
    print_header("Example 5: Error Handling and Best Practices")
    
    print_step("Demonstrating error handling patterns...")
    
    try:
        # Example 1: Handling missing API key
        try:
            voice_no_key = VoiceSecret(api_key="")
        except SecretAIAPIKeyMissingError as e:
            print_success("Correctly caught missing API key error")
        
        # Example 2: Handling connection errors
        try:
            voice_bad_host = VoiceSecret(
                stt_host="nonexistent-host.example.com",
                tts_host="nonexistent-host.example.com"
            )
            # Try to use the client
            voice_bad_host.check_stt_health()
        except (SecretAIConnectionError, Exception) as e:
            print_success(f"Correctly handled connection error: {type(e).__name__}")
        finally:
            try:
                voice_bad_host.close()
            except:
                pass
        
        # Example 3: Timeout handling
        print_step("Best practices for production usage:")
        print("✅ Always use context managers (with statement) for automatic cleanup")
        print("✅ Check service health before performing operations")
        print("✅ Handle specific exception types appropriately")
        print("✅ Set appropriate timeouts for your use case")
        print("✅ Validate audio file formats before transcription")
        print("✅ Create output directories before saving files")
        
        return True
        
    except Exception as e:
        print_error(f"Error handling demonstration failed: {e}")
        return False

def example_practical_use_case():
    """Example 6: Practical use case - Voice memo processing"""
    print_header("Example 6: Practical Use Case - Voice Memo Processing")
    
    try:
        with VoiceSecret(stt_host=VOICE_HOST, stt_port=STT_PORT,
                        tts_host=VOICE_HOST, tts_port=TTS_PORT) as voice:
            
            # Check service availability
            stt_available = tts_available = False
            try:
                voice.check_stt_health()
                stt_available = True
            except:
                pass
            
            try:
                voice.check_tts_health()
                tts_available = True
            except:
                pass
            
            if not (stt_available and tts_available):
                print_warning("Both STT and TTS services needed for this example")
                return True
            
            print_step("Simulating voice memo workflow...")
            
            output_dir = Path("voice_examples_output")
            output_dir.mkdir(exist_ok=True)
            
            # Step 1: Create a voice memo (simulated with TTS)
            memo_text = """
            Meeting notes for project Alpha: We discussed the new feature requirements 
            and decided to implement voice processing capabilities. The deadline is 
            set for next Friday. Action items: John will handle the backend integration, 
            Sarah will work on the frontend UI, and Mike will prepare the documentation.
            """
            
            print("📝 Creating voice memo...")
            memo_audio = voice.synthesize_speech(
                text=memo_text.strip(),
                model="tts-1",
                voice="af_alloy",
                response_format="wav"
            )
            memo_path = output_dir / "voice_memo.wav"
            voice.save_audio(memo_audio, memo_path)
            print_success(f"Voice memo created: {memo_path}")
            
            # Step 2: Transcribe the memo
            print("🎧 Transcribing voice memo...")
            transcription = voice.transcribe_audio(memo_path)
            transcribed_text = transcription.get('text', '')
            
            # Step 3: Save transcription
            transcript_path = output_dir / "memo_transcript.txt"
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(f"Voice Memo Transcription\n")
                f.write(f"========================\n\n")
                f.write(f"Original text:\n{memo_text.strip()}\n\n")
                f.write(f"Transcribed text:\n{transcribed_text}\n\n")
                f.write(f"Language detected: {transcription.get('language', 'unknown')}\n")
            
            print_success(f"Transcription saved: {transcript_path}")
            print(f"📄 Transcribed: '{transcribed_text[:100]}...'")
            
            # Step 4: Create summary audio
            summary = "Voice memo transcription completed successfully. Check the transcript file for full details."
            summary_audio = voice.synthesize_speech(
                text=summary,
                model="tts-1", 
                voice="af_heart",
                response_format="mp3"
            )
            summary_path = output_dir / "memo_summary.mp3"
            voice.save_audio(summary_audio, summary_path)
            print_success(f"Summary audio created: {summary_path}")
            
            print("\n🎯 Voice memo processing complete!")
            print(f"   - Original memo: {memo_path}")
            print(f"   - Transcript: {transcript_path}")
            print(f"   - Summary: {summary_path}")
        
        return True
        
    except Exception as e:
        print_error(f"Practical use case failed: {e}")
        return False

async def main():
    """Run all voice examples"""
    print("🎤 Secret AI SDK - Voice Examples")
    print("==================================")
    print(f"Configuration:")
    print(f"  Host: {VOICE_HOST}")
    print(f"  STT Port: {STT_PORT}")
    print(f"  TTS Port: {TTS_PORT}")
    print(f"  API Key: {'✅ Set' if os.getenv('SECRET_AI_API_KEY') else '❌ Missing'}")
    
    if not os.getenv('SECRET_AI_API_KEY'):
        print_error("SECRET_AI_API_KEY environment variable not set")
        print("Please set your API key: export SECRET_AI_API_KEY=your_key_here")
        return
    
    # Run examples
    examples = [
        ("Basic Setup", example_basic_setup),
        ("Service Health Checks", example_service_health_checks),
        ("TTS Capabilities", example_tts_capabilities),
        ("STT Capabilities", example_stt_capabilities),
        ("Error Handling", example_error_handling),
        ("Practical Use Case", example_practical_use_case),
    ]
    
    results = []
    for name, example_func in examples:
        try:
            result = example_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Example '{name}' failed with unexpected error: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Examples Summary")
    passed = 0
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} examples completed successfully")
    
    if passed == len(results):
        print("🎉 All examples completed successfully!")
        print("\nCheck the 'voice_examples_output' directory for generated files.")
    else:
        print("⚠️  Some examples failed - this may be due to service availability")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())