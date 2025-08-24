import os
import requests
from models import Tone, VoicePreference
import uuid
from typing import Optional

class VoiceSynthesizerSimple:
    """Voice synthesizer using direct ElevenLabs API calls"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.use_elevenlabs = api_key is not None
        self.base_url = "https://api.elevenlabs.io/v1"
        
        if self.use_elevenlabs:
            print(f"ElevenLabs API initialized with key: {api_key[:10]}...")
        else:
            print("No ElevenLabs API key provided, using text fallback")
        
        # Voice IDs for different preferences and tones (using direct voice IDs)
        self.voice_mappings = {
            VoicePreference.POETRY_LITERARY: {
                Tone.CALMED: "21m00Tcm4TlvDq8ikWAM",  # Rachel
                Tone.SPIRITUAL: "EXAVITQu4vr4xnSDxMaL",  # Bella
                Tone.CONVERSATIONAL: "MF3mGyEYCl7XYWbV9V6O",  # Elli
            },
            VoicePreference.AUTHENTIC_PRIMAL: {
                Tone.CALMED: "TxGEqnHWrfWFTfGW9XjX",  # Josh
                Tone.SPIRITUAL: "ErXwobaYiN019PkySvjV",  # Antoni
                Tone.CONVERSATIONAL: "pNInz6obpgDQGcFmaJgB",  # Adam
            }
        }

    async def generate_voice(self, script: str, tone: Tone, voice_type: VoicePreference) -> str:
        if self.use_elevenlabs and self.api_key:
            return await self._generate_with_elevenlabs(script, tone, voice_type)
        else:
            return await self._generate_fallback(script, tone, voice_type)

    async def _generate_with_elevenlabs(self, script: str, tone: Tone, voice_type: VoicePreference) -> str:
        try:
            voice_id = self.voice_mappings[voice_type][tone]
            
            # Direct API call to ElevenLabs
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                filename = f"hypnosis_{uuid.uuid4().hex}.mp3"
                filepath = f"static/audio/{filename}"
                
                os.makedirs("static/audio", exist_ok=True)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return f"/static/audio/{filename}"
            else:
                print(f"ElevenLabs API error: {response.status_code} - {response.text}")
                return await self._generate_fallback(script, tone, voice_type)
            
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


    def get_available_voices(self):
        """Get list of available voices"""
        if not self.use_elevenlabs:
            return "ElevenLabs not configured"
            
        # Return the predefined voice mappings
        voices = []
        for voice_type, tone_voices in self.voice_mappings.items():
            for tone, voice_id in tone_voices.items():
                voices.append((f"{voice_type.value}_{tone.value}", voice_id))
        return voices