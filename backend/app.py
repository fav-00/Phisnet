from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.pkl")


def extract_features(url):
    return [
        len(url),
        url.count("."),
        url.count("-"),
        url.count("@"),
        int("https" in url),
        int("http://" in url),
        int(bool(re.search(r"\d", url))),
        len(url.split("/")),
    ]


@app.post("/predict")
def predict(data: dict):
    url = data["url"]

    features = extract_features(url)

    prediction = model.predict([features])[0]

    
    return {"prediction": int(prediction)}