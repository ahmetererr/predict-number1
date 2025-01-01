from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
import numpy as np
from app.models.digit_recognizer import DigitRecognizer
from app.config import settings

app = FastAPI(title="Digit Recognition API")

# CORS middleware configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://predict-number1-frontend.onrender.com",
    "https://predict-number1.onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Initialize the digit recognizer model
model = DigitRecognizer()

@app.get("/")
async def root():
    return {"message": "Digit Recognition API is running"}

@app.post("/predict")
async def predict_digit(image: UploadFile = File(...)):
    try:
        # Read and process the image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert('L')
        
        # Make prediction
        digit, confidence = model.predict(img)
        
        return {
            "predicted_digit": int(digit),
            "confidence": float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
async def train_model(image: UploadFile = File(...), digit: int = File(...)):
    try:
        # Read and process the image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert('L')
        
        # Train the model
        success = model.train(img, digit)
        if not success:
            raise HTTPException(status_code=500, detail="Training failed")
        
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 