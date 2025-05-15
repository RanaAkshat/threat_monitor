from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Threat Monitor API is running"}


@app.get("/api/threats")
def get_threats():
    csv_path = Path("data/categorized_tweets.csv")
    if not csv_path.exists():
        return {"error": "categorized_tweets.csv not found."}

    try:
        df = pd.read_csv(csv_path)
        data = df.to_dict(orient="records")
        return {"tweets": data}
    except Exception as e:
        return {"error": f"Failed to read categorized_tweets.csv: {str(e)}"}

