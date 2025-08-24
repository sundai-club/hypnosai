import os
import requests
from typing import Optional
from models import UserInput, ScriptType, Tone, BeliefOrientation, VoicePreference

class AIScriptGenerator:
    def __init__(self, gemini_api_key: Optional[str] = None):
        self.gemini_api_key = gemini_api_key
        self.use_ai = gemini_api_key is not None
        
        if not self.use_ai:
            print("Warning: No Gemini API key provided. Using template-based generation.")
    
    def generate_script(self, user_input: UserInput) -> str:
        if self.use_ai and self.gemini_api_key:
            return self._generate_with_ai(user_input)
        else:
            return self._generate_with_templates(user_input)
    
    def _generate_with_ai(self, user_input: UserInput) -> str:
        """Generate hypnosis script using Gemini AI with the comprehensive prompt"""
        
        # Use custom goal if provided, otherwise map script types to goals
        if user_input.custom_goal and user_input.custom_goal.strip():
            goal = user_input.custom_goal.strip()
        else:
            goal_mapping = {
                ScriptType.TEST: "general relaxation and stress relief",
                ScriptType.FLIGHT: "elevated perspective and freedom from limitations", 
                ScriptType.NEXT: "embracing new beginnings and positive change",
                ScriptType.LOW: "deep relaxation and inner peace"
            }
            goal = goal_mapping[user_input.script_type]
        
        # Map predisposition scores to susceptibility levels
        if user_input.predisposition_score:
            if user_input.predisposition_score >= 65:
                susceptibility = "High"
            elif user_input.predisposition_score >= 45:
                susceptibility = "Medium"
            else:
                susceptibility = "Low"
        else:
            susceptibility = "Medium"
        
        # Build the comprehensive prompt
        prompt = f"""Create a hypnosis script for <name = {user_input.name}, age = {user_input.age}, gender = {user_input.gender.value}, personality = {user_input.personality}, belief orientation = {user_input.belief_orientation.value}, tone = {user_input.tone.value}, poetic-literary = {user_input.voice_preference == VoicePreference.POETRY_LITERARY}, authoritative-permissive = permissive, susceptibility = {susceptibility}, goal = {goal}> the only thing output should be the text that is read out loud and any [pauses] in it.

1. Induction (Stage 1) – Relaxation & Focus

The script begins with the Induction phase, aiming to gently capture the listener's attention, build rapport, and guide them into initial relaxation. Start with a warm, friendly greeting to establish rapport and safety. Guide the listener to close their eyes and focus their attention inward using progressive muscle relaxation. Incorporate breathing cues and mindfulness with slow, deep breaths. Begin using descriptive imagery to engage the imagination early with a serene scene. Use positive and permissive language throughout ("allow yourself to relax" rather than commands).

2. Deepening (Stage 2) – Intensification of Trance

Use explicit deepening suggestions with phrases like "deeper and deeper," "further down," "more and more relaxed." Incorporate a countdown from 10 to 1 or similar structured deepening method, where each number doubles relaxation. Use fractionation techniques if appropriate - briefly bringing partially out then back deeper. Expand on imagery for deepening and suggest loss of awareness of surroundings. Maintain gentle tone, possibly slowing pace as trance deepens.

3. Goal-Specific Suggestion Segment (Stage 3) – Therapeutic Suggestions & Imagery

Address the specific goal directly with positive suggestions and affirmations phrased positively and in present/near-future tense. Use metaphors and imagery related to the goal. Leverage future pacing - having the listener mentally rehearse successful future scenarios. Incorporate indirect therapeutic techniques like brief anecdotes or stories. Cover multiple angles of the goal comprehensively. Maintain hypnotic tone throughout.

4. Emergence (Stage 4) – Reorientation/Waking Up

Since this is for {user_input.script_type.value} (not sleep), include emergence. Gently signal the session is ending. Count up from 1 to 5, telling listener they'll be fully awake, refreshed and alert at 5. Include grounding and affirmation after the count. Ensure emergence is gradual and gentle, never abrupt.

Personalization Guidelines:
- Adjust for {user_input.belief_orientation.value} belief orientation: {"Use spiritual language, energy concepts, divine references" if user_input.belief_orientation == BeliefOrientation.SPIRITUAL else "Use scientific/medical terminology, neuroplasticity concepts" if user_input.belief_orientation == BeliefOrientation.SCIENTIFIC else "Use neutral, universally appealing language"}
- Use {user_input.tone.value} tone: {"Incorporate spiritual concepts, soulful style, divine light, energy" if user_input.tone == Tone.SPIRITUAL else "Sound like friendly conversation, casual reassurances, personal asides" if user_input.tone == Tone.CONVERSATIONAL else "Professional, straightforward, possibly mild technical terms"}
- Voice preference {user_input.voice_preference.value}: {"Rich descriptive language, rhythmic phrases, elegant metaphors, poetic imagery" if user_input.voice_preference == VoicePreference.POETRY_LITERARY else "Direct, authentic, grounded language that resonates deeply"}
- Susceptibility level {susceptibility}: {"Use longer, more repetitive induction and deepening, extra reassurances, indirect suggestions, go slow and steady" if susceptibility == "Low" else "Use rapid or advanced techniques, brief induction, more direct suggestions, complex techniques" if susceptibility == "High" else "Use standard balanced approach of direct and indirect methods"}

Personality adaptation for "{user_input.personality}":
- Include specific references that acknowledge their personality traits
- Use language and metaphors that would resonate with their described characteristics

The script should be approximately {user_input.duration_minutes} minutes when read aloud (roughly 150-200 words per minute of speech). Include natural [pause] markers where appropriate for breathing and integration.

Output only the spoken script text with [pause] markers. Do not include stage headings or explanations."""

        try:
            # Call Gemini API
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 4000,
                        "topP": 0.9,
                        "topK": 40
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text'].strip()
                else:
                    print("Warning: No content in AI response, using template fallback")
                    return self._generate_with_templates(user_input)
            else:
                print(f"Warning: AI API error {response.status_code}, using template fallback")
                return self._generate_with_templates(user_input)
                
        except Exception as e:
            print(f"Warning: AI generation failed ({str(e)}), using template fallback")
            return self._generate_with_templates(user_input)
    
    def _generate_with_templates(self, user_input: UserInput) -> str:
        """Fallback template-based generation"""
        # This is a simplified version of the original template system
        script_parts = []
        
        # Induction
        script_parts.append(f"Welcome, {user_input.name}. Find a comfortable position and allow yourself to settle in.")
        script_parts.append("[pause]")
        script_parts.append("Take a deep breath in... and slowly breathe out. With each breath, feel yourself becoming more relaxed and at peace.")
        script_parts.append("[pause]")
        
        # Predisposition adaptation
        if user_input.predisposition_score:
            if user_input.predisposition_score >= 80:
                script_parts.append("Your mind naturally opens to this experience, like a flower blooming in the warm sunlight.")
            elif user_input.predisposition_score >= 65:
                script_parts.append("You have a natural ability to let go and allow this peaceful experience to unfold.")
            elif user_input.predisposition_score >= 45:
                script_parts.append("Take your time to settle in, allowing yourself to become more comfortable with each breath.")
            else:
                script_parts.append("There's no pressure here, just gentle relaxation at your own natural pace.")
        
        script_parts.append("[pause]")
        
        # Deepening
        script_parts.append("Now, going deeper with each breath. I'll count down from 10 to 1, and with each number, feel yourself sinking twice as deep into relaxation.")
        script_parts.append("10... deeper relaxed... 9... letting go completely... 8... sinking further down...")
        script_parts.append("[pause]")
        script_parts.append("7... 6... 5... deeper and deeper... 4... 3... 2... and 1... perfectly relaxed.")
        script_parts.append("[pause]")
        
        # Goal-specific suggestions based on script type
        if user_input.script_type == ScriptType.FLIGHT:
            script_parts.append("Imagine yourself gently lifting off, becoming light as air, soaring above all earthly concerns.")
        elif user_input.script_type == ScriptType.NEXT:
            script_parts.append("You stand at the threshold of exciting new possibilities, ready to embrace positive change.")
        elif user_input.script_type == ScriptType.LOW:
            script_parts.append("Sinking into the deepest, most peaceful levels of consciousness, where healing naturally occurs.")
        else:
            script_parts.append("In this peaceful state, your subconscious mind is open to positive growth and change.")
        
        script_parts.append("[pause]")
        
        # Belief orientation adaptation
        if user_input.belief_orientation == BeliefOrientation.SPIRITUAL:
            script_parts.append("Connect with the divine wisdom within you, feeling guided and supported by universal love.")
        elif user_input.belief_orientation == BeliefOrientation.SCIENTIFIC:
            script_parts.append("Your mind's natural neuroplasticity allows for positive changes at the cellular level.")
        
        script_parts.append("[pause]")
        
        # Emergence
        script_parts.append("In a moment, I'll count from 1 to 5, and at 5 you'll open your eyes feeling refreshed and wonderful.")
        script_parts.append("1... beginning to return... 2... energy flowing back... 3... becoming more aware... 4... almost there... and 5... eyes open, feeling great!")
        
        return " ".join(script_parts)