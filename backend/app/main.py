from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ReadingInput, PredictionResponse
from .predictor import predict_health

app = FastAPI(title="VehicleGuard Backend", version="0.1.0")

# Allow all origins for MVP; tighten later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(reading: ReadingInput) -> PredictionResponse:
    return predict_health(reading)