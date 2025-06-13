from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import os
import requests
from transformers import pipeline

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Hugging Face classification model
classifier = pipeline("text-classification", model="unitary/unbiased-toxic-roberta", top_k=None)

# Perspective API config
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
ATTRIBUTES = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "THREAT", "IDENTITY_ATTACK"]
THRESHOLD = 0.7

# Startup message
@app.on_event("startup")
async def startup_message():
    print("✅ Backend is running and accessible at: http://127.0.0.1:8000/api/threats")

# Root check
@app.get("/")
def read_root():
    return {"message": "Threat Monitor API is running"}

# GET: Serve classified tweet data
@app.get("/api/threats")
def get_threats():
    csv_path = Path("/data/categorized_tweets.csv")
    if not csv_path.exists():
        return {"error": "categorized_tweets.csv not found."}
    try:
        df = pd.read_csv(csv_path)
        data = df.to_dict(orient="records")
        return {"tweets": data}
    except Exception as e:
        return {"error": f"Failed to read categorized_tweets.csv: {str(e)}"}

# Request body for /api/analyze
class AnalyzeRequest(BaseModel):
    text: str

# POST: Analyze tweet using HuggingFace + Perspective API
@app.post("/api/analyze")
async def analyze_text(request: AnalyzeRequest):
    text = request.text.strip().lower()

    # HuggingFace results
    local_pred = classifier(text)[0]
    local_results = {item['label']: item['score'] for item in local_pred}

    # Perspective AI results
    perspective_results = {}
    if PERSPECTIVE_API_KEY:
        try:
            data = {
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {attr: {} for attr in ATTRIBUTES}
            }
            response = requests.post(
                f"{PERSPECTIVE_API_URL}?key={PERSPECTIVE_API_KEY}",
                json=data
            )
            result = response.json()
            for attr in ATTRIBUTES:
                score = result.get("attributeScores", {}).get(attr, {}).get("summaryScore", {}).get("value", 0)
                if score >= THRESHOLD:
                    perspective_results[attr] = score
        except Exception as e:
            perspective_results["error"] = str(e)

    return {
        "local_results": local_results,
        "perspective_results": perspective_results
    }
