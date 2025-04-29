# Backend/App/Main

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import uvicorn
import numpy as np  # Also needed for np.max().

# Load model.
model = joblib.load('App/Spam_Classifier.pkl')

# App.
app = FastAPI(
    title="Spam Detector API",
    description="An API that detects spam messages.",
    version="1.0"
)

# Add CORS middleware.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict later).
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body.
class MessageRequest(BaseModel):
    message: str

# Health check.
@app.get("/Health-Check")
def healthcheck():
    return {"Status": "Ok"}

# Predict endpoint.
@app.post("/Predict")
def predict_message(data: MessageRequest):
    prediction = model.predict([data.message])[0]
    proba = model.predict_proba([data.message])[0]
    result = "Spam" if prediction == 1 else "Not Spam"
    confidence = round(np.max(proba) * 100, 2)
    return {
        "Prediction": result,
        "Confidence": confidence
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

