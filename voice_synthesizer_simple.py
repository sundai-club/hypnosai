import os
import requests
from models import Tone, VoicePreference
import uuid
from typing import Optional

class VoiceSynthesizerSimple:
    """Simplified voice synthesizer that can work without ElevenLabs if needed"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.use_elevenlabs = api_key is not None
        
        if self.use_elevenlabs:
            try:
                # Try to import and use ElevenLabs
                from elevenlabs.client import ElevenLabs
                from elevenlabs import generate, save, voices, Voice
                
                # Set up the client with API key
                self.client = ElevenLabs(api_key=api_key)
                self.generate_lib = generate
                self.save_lib = save
                self.voices_lib = voices
                self.Voice = Voice
                
                # Also set environment variable as fallback
                os.environ["ELEVENLABS_API_KEY"] = api_key
                print(f"ElevenLabs initialized with API key: {api_key[:10]}...")
            except ImportError as e:
                print(f"ElevenLabs not available: {e}, using fallback")
                self.use_elevenlabs = False
        
        # Voice mappings for different preferences and tones
        self.voice_mappings = {
            VoicePreference.POETRY_LITERARY: {
                Tone.CALMED: "Rachel",
                Tone.SPIRITUAL: "Bella",
                Tone.CONVERSATIONAL: "Elli",
            },
            VoicePreference.AUTHENTIC_PRIMAL: {
                Tone.CALMED: "Josh",
                Tone.SPIRITUAL: "Antoni", 
                Tone.CONVERSATIONAL: "Adam",
            }
        }

    async def generate_voice(self, script: str, tone: Tone, voice_type: VoicePreference) -> str:
        if self.use_elevenlabs and self.api_key:
            return await self._generate_with_elevenlabs(script, tone, voice_type)
        else:
            return await self._generate_fallback(script, tone, voice_type)

    async def _generate_with_elevenlabs(self, script: str, tone: Tone, voice_type: VoicePreference) -> str:
        try:
            voice_name = self.voice_mappings[voice_type][tone]
            
            # Try using the client first, then fall back to direct function call
            try:
                audio = self.client.generate(
                    text=script,
                    voice=self._get_voice_id(voice_name),
                    model="eleven_multilingual_v2"
                )
            except:
                # Fallback to the old method
                audio = self.generate_lib(
                    text=script,
                    voice=self.Voice(voice_id=self._get_voice_id(voice_name)),
                    model="eleven_multilingual_v2"
                )
            
            filename = f"hypnosis_{uuid.uuid4().hex}.mp3"
            filepath = f"static/audio/{filename}"
            
            os.makedirs("static/audio", exist_ok=True)
            self.save_lib(audio, filepath)
            
            return f"/static/audio/{filename}"
            
        except Exception as e:
            print(f"ElevenLabs failed: {e}, using fallback")
            return await self._generate_fallback(script, tone, voice_type)

    async def _generate_fallback(self, script: str, tone: Tone, voice_type: VoicePreference) -> str:
        """Fallback method that creates a text file instead of audio"""
        try:
            filename = f"hypnosis_script_{uuid.uuid4().hex}.txt"
            filepath = f"static/audio/{filename}"
            
            os.makedirs("static/audio", exist_ok=True)
            
            # Create a text file with the script
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Hypnosis Script ({tone.value}, {voice_type.value})\n")
                f.write("=" * 50 + "\n\n")
                f.write(script)
                f.write(f"\n\nNote: Audio generation requires ElevenLabs API key.")
            
            return f"/static/audio/{filename}"
            
        except Exception as e:
            raise Exception(f"Voice generation failed: {str(e)}")

    def _get_voice_id(self, voice_name: str) -> str:
        """Get voice ID from voice name"""
        if not self.use_elevenlabs:
            return "fallback"
            
        try:
            # Try using the client first
            try:
                all_voices = self.client.voices.get_all()
                for voice in all_voices.voices:
                    if voice.name == voice_name:
                        return voice.voice_id
                return all_voices.voices[0].voice_id if all_voices.voices else "21m00Tcm4TlvDq8ikWAM"
            except:
                # Fallback to old method
                all_voices = self.voices_lib()
                for voice in all_voices:
                    if voice.name == voice_name:
                        return voice.voice_id
                return all_voices[0].voice_id if all_voices else "21m00Tcm4TlvDq8ikWAM"
        except Exception as e:
            print(f"Voice lookup failed: {e}, using default voice")
            return "21m00Tcm4TlvDq8ikWAM"

    def get_available_voices(self):
        """Get list of available voices"""
        if not self.use_elevenlabs:
            return "ElevenLabs not configured"
            
        try:
            return [(voice.name, voice.voice_id) for voice in self.voices_lib()]
        except Exception as e:
            return f"Error fetching voices: {str(e)}"