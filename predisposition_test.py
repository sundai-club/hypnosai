from typing import List, Dict
from pydantic import BaseModel

class TestQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    scores: List[int]  # Score for each option (0-3)

class PredispositionTest:
    def __init__(self):
        self.questions = [
            TestQuestion(
                id=1,
                question="When you close your eyes and listen to music, how easily can you visualize scenes or images?",
                options=[
                    "I see vivid, detailed images almost like watching a movie",
                    "I can see some images, but they're somewhat hazy",
                    "I occasionally see brief, unclear images",
                    "I rarely or never see any images"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=2,
                question="How often do you find yourself completely absorbed in a book or movie, losing track of time?",
                options=[
                    "Very frequently - I often get completely lost in stories",
                    "Fairly often - I can get absorbed but still aware of surroundings",
                    "Sometimes - depends on how interesting it is",
                    "Rarely - I'm usually aware of everything around me"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=3,
                question="When someone gives you directions, what do you rely on most?",
                options=[
                    "I visualize the route and landmarks in my mind",
                    "I focus on the verbal instructions and repeat them",
                    "I need to write them down or use a map",
                    "I prefer to figure it out as I go"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=4,
                question="How do you typically respond to guided meditation or relaxation exercises?",
                options=[
                    "I easily follow along and feel deeply relaxed",
                    "I can follow along with some effort and feel moderately relaxed",
                    "I have difficulty concentrating but can achieve some relaxation",
                    "I find it hard to focus and don't feel very relaxed"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=5,
                question="When you're trying to fall asleep, what happens most often?",
                options=[
                    "My mind naturally quiets down and I drift off easily",
                    "I can quiet my mind with some relaxation techniques",
                    "My mind stays active but I eventually fall asleep",
                    "I often lie awake with an active, racing mind"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=6,
                question="How do you respond to suggestions about your physical sensations (like 'your arm is getting heavy')?",
                options=[
                    "I immediately notice and feel the suggested sensation",
                    "I feel the sensation after focusing on it for a moment",
                    "I sometimes feel it, but it takes concentration",
                    "I rarely feel physical sensations from suggestions"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=7,
                question="When you daydream, how realistic and detailed are your mental experiences?",
                options=[
                    "Very realistic - sometimes I forget I'm daydreaming",
                    "Fairly realistic - I can get caught up in them",
                    "Somewhat realistic - more like thinking than experiencing",
                    "Not very realistic - just vague thoughts or ideas"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=8,
                question="How easily can you remember and re-experience pleasant memories?",
                options=[
                    "I can vividly re-experience memories with all senses",
                    "I can recall memories with some sensory details",
                    "I remember events but without much sensory detail",
                    "I mostly remember facts about events, not the experience"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=9,
                question="When you're in a comfortable, quiet environment, how easily do you let your mind wander?",
                options=[
                    "Very easily - my mind naturally drifts and flows",
                    "Fairly easily - I can let go with minimal effort",
                    "With some effort - I can relax my mental control",
                    "With difficulty - I tend to stay mentally alert and focused"
                ],
                scores=[3, 2, 1, 0]
            ),
            TestQuestion(
                id=10,
                question="How do you typically respond to repetitive, rhythmic sounds (like ocean waves or drumming)?",
                options=[
                    "They immediately relax me and I often enter a trance-like state",
                    "They help me relax and I feel quite peaceful",
                    "They're somewhat relaxing but I remain alert",
                    "They don't have much effect on my mental state"
                ],
                scores=[3, 2, 1, 0]
            )
        ]
    
    def get_questions(self) -> List[TestQuestion]:
        return self.questions
    
    def calculate_score(self, answers: List[int]) -> Dict[str, any]:
        """Calculate predisposition score from answers (list of option indices)"""
        total_score = 0
        max_possible = len(self.questions) * 3
        
        for i, answer_index in enumerate(answers):
            if i < len(self.questions) and 0 <= answer_index < len(self.questions[i].scores):
                total_score += self.questions[i].scores[answer_index]
        
        percentage = (total_score / max_possible) * 100
        
        # Determine predisposition level
        if percentage >= 80:
            level = "Very High"
            description = "You have exceptional hypnotic responsiveness. You're likely to experience deep, vivid hypnotic states with ease."
        elif percentage >= 65:
            level = "High" 
            description = "You have strong hypnotic responsiveness. You should experience effective hypnotic states with good results."
        elif percentage >= 45:
            level = "Moderate"
            description = "You have moderate hypnotic responsiveness. With practice and the right approach, you can achieve beneficial hypnotic states."
        elif percentage >= 25:
            level = "Low"
            description = "You have lower hypnotic responsiveness. You may need more specialized techniques or additional practice to achieve hypnotic states."
        else:
            level = "Very Low"
            description = "You have minimal hypnotic responsiveness currently. Consider starting with basic relaxation techniques before attempting deeper hypnosis."
        
        return {
            "raw_score": total_score,
            "max_score": max_possible,
            "percentage": round(percentage, 1),
            "level": level,
            "description": description,
            "recommendations": self._get_recommendations(level)
        }
    
    def _get_recommendations(self, level: str) -> List[str]:
        """Get personalized recommendations based on predisposition level"""
        recommendations = {
            "Very High": [
                "You're ideal for all types of hypnotic experiences",
                "Consider longer, more complex hypnotic sessions",
                "Visual and sensory-rich scripts will work excellently for you",
                "You may benefit from self-hypnosis training"
            ],
            "High": [
                "Most hypnotic techniques should work well for you",
                "Progressive relaxation and visualization will be very effective",
                "You can handle moderate to long session durations",
                "Consider exploring different hypnotic themes"
            ],
            "Moderate": [
                "Start with shorter sessions and build up gradually",
                "Focus on relaxation-based approaches initially", 
                "Repetitive, rhythmic elements will help deepen your experience",
                "Practice regularly to improve your responsiveness"
            ],
            "Low": [
                "Begin with basic relaxation and breathing exercises",
                "Use shorter sessions (5-10 minutes) initially",
                "Focus on simple, direct suggestions",
                "Consider combining with meditation practice"
            ],
            "Very Low": [
                "Start with general relaxation techniques",
                "Keep sessions very short (3-5 minutes)",
                "Use simple, conversational language",
                "Focus on stress relief rather than deep hypnosis"
            ]
        }
        
        return recommendations.get(level, [])