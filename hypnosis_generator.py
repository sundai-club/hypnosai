from models import UserInput, ScriptType, Tone, BeliefOrientation, VoicePreference
import random

class HypnosisGenerator:
    def __init__(self):
        self.script_templates = {
            ScriptType.TEST: {
                "intro": [
                    "Welcome, {name}. Find a comfortable position and allow yourself to settle in.",
                    "Hello {name}, let's begin this journey together. Take a moment to breathe deeply.",
                    "{name}, as you prepare for this experience, know that you are in complete control."
                ],
                "deepening": [
                    "With each breath, feel yourself becoming more relaxed and at peace.",
                    "Notice how your body naturally knows how to let go of tension.",
                    "Allow your mind to drift into a state of gentle focus and calm awareness."
                ],
                "suggestions": [
                    "Your subconscious mind is open to positive change and growth.",
                    "You have within you all the resources you need for success and happiness.",
                    "Trust in your inner wisdom to guide you toward your highest good."
                ],
                "awakening": [
                    "In a moment, you'll return to full awareness, feeling refreshed and renewed.",
                    "Take these feelings of peace and confidence with you into your day.",
                    "On the count of three, you'll open your eyes feeling wonderful. One... two... three."
                ]
            },
            ScriptType.FLIGHT: {
                "intro": [
                    "{name}, imagine yourself preparing for a beautiful journey through the clouds.",
                    "Close your eyes, {name}, and feel yourself becoming light as air.",
                    "Welcome aboard this peaceful flight, {name}. Your destination is deep relaxation."
                ],
                "deepening": [
                    "Feel yourself gently lifting off, leaving all earthly concerns below.",
                    "As you soar higher, notice how free and weightless you become.",
                    "The clouds embrace you softly as you float through this serene sky."
                ],
                "suggestions": [
                    "From this elevated perspective, see how small your worries truly are.",
                    "You have the power to rise above any challenge or obstacle.",
                    "Like a bird in flight, you move through life with grace and ease."
                ],
                "awakening": [
                    "Now gently descend back to earth, carrying this sense of freedom with you.",
                    "Feel your feet touching solid ground, grounded yet transformed.",
                    "Open your eyes when ready, feeling uplifted and inspired."
                ]
            },
            ScriptType.NEXT: {
                "intro": [
                    "{name}, this moment marks the beginning of your next chapter.",
                    "Step forward with me, {name}, into the possibilities that await.",
                    "You stand at a threshold, {name}, ready to embrace what comes next."
                ],
                "deepening": [
                    "Feel the excitement of new beginnings flowing through you.",
                    "Your mind opens to fresh perspectives and opportunities.",
                    "Each breath brings you closer to your emerging future self."
                ],
                "suggestions": [
                    "You are ready to embrace change with courage and confidence.",
                    "The next phase of your life unfolds with perfect timing.",
                    "Trust that each step forward leads you to greater fulfillment."
                ],
                "awakening": [
                    "Return now with a clear vision of your path ahead.",
                    "Feel the energy and motivation to take your next steps.",
                    "Open your eyes, ready to create the future you desire."
                ]
            },
            ScriptType.LOW: {
                "intro": [
                    "{name}, allow yourself to sink into the deepest levels of relaxation.",
                    "Go deeper now, {name}, into the quiet sanctuary of your inner mind.",
                    "Descend with me, {name}, into the peaceful depths of consciousness."
                ],
                "deepening": [
                    "Feel yourself sinking deeper with each word I speak.",
                    "Your conscious mind rests while your deeper wisdom awakens.",
                    "In this profound state, healing and transformation naturally occur."
                ],
                "suggestions": [
                    "At this deep level, positive changes integrate effortlessly.",
                    "Your subconscious mind embraces these suggestions completely.",
                    "Deep within, you find the strength and clarity you seek."
                ],
                "awakening": [
                    "Slowly now, begin your gentle return to surface consciousness.",
                    "Bring with you the deep peace and insights from this journey.",
                    "Emerge refreshed, renewed, and deeply transformed."
                ]
            }
        }

    def generate_script(self, user_input: UserInput) -> str:
        template = self.script_templates[user_input.script_type]
        
        # Personalize the script
        script_parts = []
        
        # Add intro
        intro = random.choice(template["intro"]).format(name=user_input.name)
        script_parts.append(intro)
        
        # Add predisposition-based customization
        if user_input.predisposition_score and user_input.predisposition_level:
            if user_input.predisposition_score >= 80:
                script_parts.append("Your mind naturally opens to this experience, like a flower blooming in the warm sunlight.")
            elif user_input.predisposition_score >= 65:
                script_parts.append("You have a natural ability to let go and allow this peaceful experience to unfold.")
            elif user_input.predisposition_score >= 45:
                script_parts.append("Take your time to settle in, allowing yourself to become more comfortable with each breath.")
            else:
                script_parts.append("There's no pressure here, just gentle relaxation at your own natural pace.")
        
        # Add personality-based customization
        if "anxious" in user_input.personality.lower() or "nervous" in user_input.personality.lower():
            script_parts.append("Notice how your breathing naturally slows and deepens, washing away any tension or worry.")
        elif "energetic" in user_input.personality.lower() or "active" in user_input.personality.lower():
            script_parts.append("Even your vibrant energy can find perfect balance in this peaceful state.")
        
        # Add belief-oriented language
        if user_input.belief_orientation == BeliefOrientation.SPIRITUAL:
            script_parts.append("Connect with the divine wisdom within you, feeling guided and supported by universal love.")
        elif user_input.belief_orientation == BeliefOrientation.SCIENTIFIC:
            script_parts.append("Your mind's natural neuroplasticity allows for positive changes at the cellular level.")
        
        # Add deepening with predisposition awareness
        deepening = random.choice(template["deepening"])
        script_parts.append(deepening)
        
        # Additional deepening based on predisposition
        if user_input.predisposition_score:
            if user_input.predisposition_score >= 65:
                script_parts.append("Going deeper now, twice as deep, feeling completely safe and comfortable.")
            elif user_input.predisposition_score >= 45:
                script_parts.append("Continuing to relax more deeply, at exactly the right pace for you.")
            else:
                script_parts.append("Simply enjoying this peaceful feeling, relaxing as much as feels comfortable.")
        
        # Add tone-specific language
        if user_input.tone == Tone.SPIRITUAL:
            script_parts.append("Feel your soul expanding with light and love, connected to all that is.")
        elif user_input.tone == Tone.CONVERSATIONAL:
            script_parts.append("You know, it's amazing how your mind can shift so naturally into this peaceful state.")
        else:  # CALMED
            script_parts.append("Pure tranquility flows through every cell of your being.")
        
        # Add suggestions with predisposition adaptation
        suggestions = random.choice(template["suggestions"])
        script_parts.append(suggestions)
        
        # Add predisposition-specific reinforcement
        if user_input.predisposition_score:
            if user_input.predisposition_score >= 80:
                script_parts.append("These positive suggestions integrate effortlessly into your subconscious mind, becoming part of your natural way of being.")
            elif user_input.predisposition_score >= 45:
                script_parts.append("Allow these positive ideas to settle gently into your awareness, taking root and growing stronger.")
            else:
                script_parts.append("Consider these positive thoughts as gentle suggestions that you can accept at your own pace.")
        
        # Add voice preference influence
        if user_input.voice_preference == VoicePreference.POETRY_LITERARY:
            script_parts.append("Like verses of an ancient poem, these words weave through your consciousness, creating harmony and beauty within.")
        else:  # AUTHENTIC_PRIMAL
            script_parts.append("This truth resonates in your bones, in the very essence of who you are.")
        
        # Add awakening with predisposition consideration
        awakening = random.choice(template["awakening"])
        script_parts.append(awakening)
        
        # Final awakening based on predisposition
        if user_input.predisposition_score and user_input.predisposition_score >= 65:
            script_parts.append("Take a moment to fully integrate this experience before opening your eyes completely alert and refreshed.")
        
        return " ".join(script_parts)