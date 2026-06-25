from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import math
import re
from collections import Counter

def entropy(url):
    p, lns = Counter(url), float(len(url))
    return -sum(count/lns * math.log2(count/lns) for count in p.values())

app = FastAPI(title="Phishing Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models = {
    "Random Forest": joblib.load("rf_model.pkl"),
    "Gradient Boosting": joblib.load("gb_model.pkl"),
    "Logistic Regression": joblib.load("lr_model.pkl"),
    "SVM": joblib.load("svm_model.pkl")
}
scaler = joblib.load("scaler.pkl")

def extract_features(url):
    url = str(url).lower()
    domain_split = url.split("://")[-1].split("/")
    domain = domain_split[0] if len(domain_split) > 0 else url
    return [
        len(url),
        len(domain),
        url.count("."),
        url.count("-"),
        url.count("@"),
        url.count("?"),
        url.count("&"),
        url.count("="),
        url.count("%"),
        url.count("_"),
        url.count(":"),
        url.count("#"),
        url.count("~"),
        url.count("/"),
        len(domain.split(".")) - 2 if len(domain.split(".")) > 2 else 0,
        len(domain.split(".")[-1]) if "." in domain else 0,
        domain.count("-"),
        sum(c.isdigit() for c in url),
        len(set(url)),
        entropy(url),
        int(url.startswith("https://")),
        int(url.startswith("http://")),
        int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url))),
        int(".." in url),
        int("//" in url[8:] if len(url) > 8 else False),
        int(any(s in url for s in [
            "bit.ly",
            "tinyurl",
            "t.co",
            "goo.gl"
        ])),
        int(len(domain) > 30),
        int(len(url) > 75),
        int(len(url.split("/")) > 5),
        int("xn--" in domain),
        sum(word in url for word in [
            "login",
            "signin",
            "verify",
            "secure",
            "update",
            "account",
            "bank",
            "confirm",
            "password"
        ]),
        int(any(b in url for b in [
            "paypal",
            "google",
            "amazon",
            "microsoft",
            "facebook",
            "apple"
        ])),
        int(bool(re.search(
            r"(login|verify|secure|account).*\d",
            url
        ))),
        int(domain.count("-") > 2),
        int(url.count(".") > 3),
        int(bool(re.search(
            r"[a-zA-Z]{10,}\d{3,}",
            url
        ))),
        int(bool(re.search(
            r"free|bonus|gift|reward|claim",
            url
        ))),
        int(bool(re.search(
            r"verify-account|secure-login|update-info",
            url
        )))
    ]

class URLRequest(BaseModel):
    url: str
    model_name: str = "Random Forest"

@app.post("/predict")
def predict(data: dict):
    url = data["url"]
    model_name = data.get("model_name", "Random Forest")
    features = scaler.transform([extract_features(url)])
    model = models[model_name]
    prediction = model.predict(features)[0]
    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(features)[0][1])
    else:
        proba = None

    return {
        "model": model_name,
        "prediction": int(prediction),
        "label": "Phishing" if prediction == 1 else "Legitimate",
        "probability": float(proba) if proba is not None else None
    }

@app.post("/compare")
def compare_models(request: URLRequest):
    raw = extract_features(request.url)
    features = scaler.transform([raw])
    print("RAW FEATURES:", raw) # DEBUG LINE - delete after testing

    results = []
    for name, model in models.items():
        pred = int(model.predict(features)[0])
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba(features)[0][1])
        else:
            proba = None
        results.append({
            "model": name,
            "prediction": pred,
            "label": "Phishing" if pred == 1 else "Legitimate",
            "probability": proba,
            "confidence": (proba if pred == 1 else (1 - proba)) if proba is not None else None
        })
    return {"url": request.url, "results": results}

@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": list(models.keys())}