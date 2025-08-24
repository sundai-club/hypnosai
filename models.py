from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class BeliefOrientation(str, Enum):
    SPIRITUAL = "spiritual"
    SCIENTIFIC = "scientific"
    NEUTRAL = "neutral"

class Tone(str, Enum):
    CALMED = "calmed"
    SPIRITUAL = "spiritual"
    CONVERSATIONAL = "conversational"

class ScriptType(str, Enum):
    TEST = "test"
    FLIGHT = "flight"
    NEXT = "next"
    LOW = "low"

class VoicePreference(str, Enum):
    POETRY_LITERARY = "poetry_literary"
    AUTHENTIC_PRIMAL = "authentic_primal"

class UserInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=18, le=100)
    gender: Gender
    personality: str = Field(..., min_length=10, max_length=500)
    belief_orientation: BeliefOrientation
    tone: Tone
    script_type: ScriptType = ScriptType.TEST
    voice_preference: VoicePreference = VoicePreference.AUTHENTIC_PRIMAL
    duration_minutes: Optional[int] = Field(default=10, ge=5, le=60)
    predisposition_score: Optional[float] = Field(default=None, ge=0, le=100)
    predisposition_level: Optional[str] = Field(default=None)

class HypnosisResponse(BaseModel):
    script: str
    audio_url: str
    duration_estimate: float
    script_type: ScriptType