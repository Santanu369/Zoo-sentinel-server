from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
import os
import resend


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load our trained model
model = joblib.load("zoo_sentinel_model.pkl")


class PredictionInput(BaseModel):
    animal: str
    behaviour: str
    intensity: float
    abnormality_percentage: float
    duration_minutes: float


@app.get("/")
def home():
    return {"message": "Zoo Sentinel ML server is running"}


@app.post("/predict")
def predict(data: PredictionInput):

    input_data = pd.DataFrame([{
        "Animal_Name": data.animal,
        "Behaviour": data.behaviour,
        "Intensity": data.intensity,
        "Abnormality_Percentage": data.abnormality_percentage,
        "Duration_Minutes": data.duration_minutes
    }])

    prediction = model.predict(input_data)[0]

    return {
        "hazard_probability": round(float(prediction), 2)
    }

@app.get("/sendEmail")
def send_email():
    resend.api_key = os.getenv("RESEND_API")

    r = resend.Emails.send({
    "from": "onboarding@resend.dev",
    "to": "rajranjan.ju29@gmail.com",
    "subject": "Emergency Alert",
    "html": """
        <h2>Emergency Alert</h2>
        <p>Unusual animal behaviour has been detected.</p>
        <p>Please check your area.</p>
    """
    })



    return {
        "status": "Email sent",
    }
