# app/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import PredictResponse, FeedbackRequest
from app.model import load_model, preprocess_image, CLASS_NAMES
import numpy as np
import pandas as pd
from datetime import datetime
import os

app = FastAPI(title="GreenVision API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()

@app.get("/", tags=["default"])
async def root():
    return {"message": "¡Hola! GreenVision API está viva 🥰"}

@app.post("/predict", response_model=PredictResponse, tags=["predicción"])
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Porfa sube un archivo de imagen.")
    contents = await file.read()
    try:
        arr = preprocess_image(contents)
    except Exception as e:
        raise HTTPException(500, f"Error al procesar imagen: {e}")
    preds = model.predict(arr)
    idx = int(np.argmax(preds[0]))
    label = CLASS_NAMES[idx]
    confidence = float(preds[0][idx])
    return PredictResponse(label=label, confidence=confidence)

@app.post("/feedback", tags=["feedback"])
async def feedback(fb: FeedbackRequest):
    os.makedirs("feedback", exist_ok=True)
    log_path = "feedback/feedback_log.csv"
    df = pd.DataFrame([{
        "timestamp": datetime.utcnow().isoformat(),
        "predicted": fb.predicted,
        "correct": fb.correct
    }])
    header = not os.path.isfile(log_path)
    df.to_csv(log_path, mode="a", header=header, index=False)
    return {"message": "¡Feedback recibido, gracias por ayudarme! 💚" }
