from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

from models import UserInput, HypnosisResponse
from hypnosis_generator import HypnosisGenerator
from voice_synthesizer import VoiceSynthesizer
from predisposition_test import PredispositionTest
from typing import List

load_dotenv()

app = FastAPI(title="HypnosAI", description="AI-powered hypnosis generation")

hypnosis_generator = HypnosisGenerator()
voice_synthesizer = VoiceSynthesizer(api_key=os.getenv("ELEVENLABS_API_KEY"))
predisposition_test = PredispositionTest()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/app.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/test-questions")
async def get_test_questions():
    return predisposition_test.get_questions()

@app.post("/api/calculate-score")
async def calculate_score(request: dict):
    answers = request.get("answers", [])
    return predisposition_test.calculate_score(answers)

@app.post("/generate-hypnosis", response_model=HypnosisResponse)
async def generate_hypnosis(user_input: UserInput):
    try:
        script = hypnosis_generator.generate_script(user_input)
        audio_url = await voice_synthesizer.generate_voice(
            script=script,
            tone=user_input.tone,
            voice_type=user_input.voice_preference
        )
        
        return HypnosisResponse(
            script=script,
            audio_url=audio_url,
            duration_estimate=len(script.split()) * 0.6,  # rough estimate
            script_type=user_input.script_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)