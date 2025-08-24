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
        """Generate hypnosis script using Gemini AI with the comprehensive prompt from prompt.txt"""
        
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
        
        try:
            # Read the comprehensive prompt from prompt.txt
            with open('prompt.txt', 'r', encoding='utf-8') as f:
                base_prompt = f.read()
            
            # Replace the placeholders in the prompt with user data, handling None values
            prompt = base_prompt.replace('<name = ', f'<name = {user_input.name or "Guest"}')
            prompt = prompt.replace('age = ', f'age = {user_input.age or "not specified"}')
            prompt = prompt.replace('gender = ', f'gender = {user_input.gender.value if user_input.gender else "not specified"}')
            prompt = prompt.replace('personality = ', f'personality = {user_input.personality or "not specified"}')
            prompt = prompt.replace('belief orientation = ', f'belief orientation = {user_input.belief_orientation.value if user_input.belief_orientation else "neutral"}')
            prompt = prompt.replace('tone = ', f'tone = {user_input.tone.value if user_input.tone else "calmed"}')
            prompt = prompt.replace('poetic-literary =', f'poetic-literary = {user_input.voice_preference == VoicePreference.POETRY_LITERARY}')
            prompt = prompt.replace('authoritative-permissive = ', f'authoritative-permissive = permissive')
            prompt = prompt.replace('susceptibility =', f'susceptibility = {susceptibility}')
            prompt = prompt.replace('goal =  >', f'goal = {goal}>')
            
        except FileNotFoundError:
            print("Warning: prompt.txt not found, using fallback generation")
            return self._generate_with_templates(user_input)

        try:
            # Call Gemini API with the prompt from file
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_api_key}",
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
        """Fallback template-based generation with graceful handling of missing data"""
        # This is a simplified version of the original template system
        script_parts = []
        
        # Use name or default to "Guest"
        name = user_input.name or "Guest"
        
        # Induction
        script_parts.append(f"Welcome, {name}. Find a comfortable position and allow yourself to settle in.")
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
        else:
            script_parts.append("Allow yourself to relax at whatever pace feels natural and comfortable for you.")
        
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
        
        # Belief orientation adaptation (handle None values)
        if user_input.belief_orientation == BeliefOrientation.SPIRITUAL:
            script_parts.append("Connect with the divine wisdom within you, feeling guided and supported by universal love.")
        elif user_input.belief_orientation == BeliefOrientation.SCIENTIFIC:
            script_parts.append("Your mind's natural neuroplasticity allows for positive changes at the cellular level.")
        else:
            script_parts.append("Trust in your inner wisdom and natural ability to heal and grow.")
        
        script_parts.append("[pause]")
        
        # Emergence
        script_parts.append("In a moment, I'll count from 1 to 5, and at 5 you'll open your eyes feeling refreshed and wonderful.")
        script_parts.append("1... beginning to return... 2... energy flowing back... 3... becoming more aware... 4... almost there... and 5... eyes open, feeling great!")
        
        return " ".join(script_parts)