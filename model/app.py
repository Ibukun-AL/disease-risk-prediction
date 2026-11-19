from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

N_FEATURES = 30
app = FastAPI(title="Risk model service")
_model = joblib.load(Path(__file__).parent / "model.pkl")


class PredictIn(BaseModel):
    features: list[float] = Field(min_length=N_FEATURES, max_length=N_FEATURES)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(body: PredictIn):
    risk = float(_model.predict_proba([body.features])[0][1])
    return {"risk": risk, "label": "higher" if risk >= 0.5 else "lower"}
