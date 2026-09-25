from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your trained model
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

@app.get("/sendSMS")
def sendSMS():
    account_sid = "YOUR_ACCOUNT_SID"
    auth_token = "YOUR_AUTH_TOKEN"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Emergency alert! Please check your area.",
        from_="+918250038439",
        to="+919093654355"
    )

    return {
        "status": "SMS sent",
        "sid": message.sid
    }


