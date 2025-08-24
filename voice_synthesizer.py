import os
import requests
from elevenlabs import generate, save, voices, Voice
from models import Tone, VoicePreference
import uuid
from typing import Optional

class VoiceSynthesizer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        os.environ["ELEVENLABS_API_KEY"] = api_key
        
        # Voice mappings for different preferences and tones
        self.voice_mappings = {
            VoicePreference.POETRY_LITERARY: {
                Tone.CALMED: "Rachel",  # Soft, articulate voice
                Tone.SPIRITUAL: "Bella", # Warm, nurturing voice
                Tone.CONVERSATIONAL: "Elli", # Natural, friendly voice
            },
            VoicePreference.AUTHENTIC_PRIMAL: {
                Tone.CALMED: "Josh", # Deep, grounding voice
                Tone.SPIRITUAL: "Antoni", # Rich, resonant voice
                Tone.CONVERSATIONAL: "Adam", # Natural, conversational voice
            }
        }
        
        # Voice settings for hypnosis
        self.voice_settings = {
            "stability": 0.8,  # Higher stability for consistent tone
            "similarity_boost": 0.7,  # Maintain voice character
            "style": 0.3,  # Subtle style for hypnosis
            "use_speaker_boost": True
        }

    async def generate_voice(self, script: str, tone: Tone, voice_type: VoicePreference) -> str:
        try:
            # Select appropriate voice
            voice_name = self.voice_mappings[voice_type][tone]
            
            # Generate audio
            audio = generate(
                text=script,
                voice=Voice(voice_id=self._get_voice_id(voice_name)),
                model="eleven_multilingual_v2"
            )
            
            # Save audio file
            filename = f"hypnosis_{uuid.uuid4().hex}.mp3"
            filepath = f"static/audio/{filename}"
            
            # Ensure directory exists
            os.makedirs("static/audio", exist_ok=True)
            
            # Save the audio
            save(audio, filepath)
            
            return f"/static/audio/{filename}"
            
        except Exception as e:
            # Fallback: return a placeholder or raise error
            raise Exception(f"Voice generation failed: {str(e)}")

    def _get_voice_id(self, voice_name: str) -> str:
        """Get voice ID from voice name"""
        try:
            all_voices = voices()
            for voice in all_voices:
                if voice.name == voice_name:
                    return voice.voice_id
            # Fallback to first available voice
            return all_voices[0].voice_id if all_voices else "21m00Tcm4TlvDq8ikWAM"
        except:
            # Hardcoded fallback voice ID (Rachel)
            return "21m00Tcm4TlvDq8ikWAM"

    def get_available_voices(self):
        """Get list of available voices for debugging"""
        try:
            return [(voice.name, voice.voice_id) for voice in voices()]
        except Exception as e:
            return f"Error fetching voices: {str(e)}"