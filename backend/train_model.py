from pyexpat import features

import pandas as pd
import numpy as np
import re
import math
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.svm import LinearSVC

import joblib


def entropy(url):
    p = Counter(url)
    lns = float(len(url))
    return -sum(count / lns * math.log2(count / lns) for count in p.values())


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


df = pd.read_csv("data/new_data_urls.csv")

df = df.dropna().drop_duplicates()
df.columns = ["url", "label"]

print("Original:", df.shape)
df, _ = train_test_split(
    df,
    train_size=20000,
    stratify=df["label"],
    random_state=42
)
print("Sampled:", df.shape)

print("\nLABEL DISTRIBUTION:")
print(df["label"].value_counts(normalize=True) * 100)

X = np.array(df["url"].apply(extract_features).tolist())
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

joblib.dump(scaler, "scaler.pkl")

sample_weights = compute_sample_weight("balanced", y_train)

models = {
    "lr_model": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),

    "rf_model": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),

    "gb_model": GradientBoostingClassifier(
        random_state=42
    ),

    "svm_model": LinearSVC(
        class_weight="balanced",
        random_state=42
    )
}

results = []

for name, model in models.items():

    print(f"\nTraining {name}...")

    if name == "gb_model":
        model.fit(X_train, y_train, sample_weight=sample_weights)
    else:
        model.fit(X_train, y_train)

    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds, zero_division=0)
    recall = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

    print("\n" + "=" * 60)
    print(f"{name.upper()} PERFORMANCE")
    print("=" * 60)

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nCONFUSION MATRIX")
    print(f"True Negatives (TN): {tn}")
    print(f"False Positives (FP): {fp}")
    print(f"False Negatives (FN): {fn}")
    print(f"True Positives (TP): {tp}")

    results.append({
        "Model": name.replace("_model", "").upper(),
        "Accuracy": round(accuracy, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1 Score": round(f1, 4),
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp
    })

    joblib.dump(model, f"{name}.pkl")
    print(f"\nSaved {name}.pkl")

results_df = pd.DataFrame(results)

results_df.to_csv("model_metrics.csv", index=False)


print("\nMODEL COMPARISON:")
print(results_df.to_string(index=False))

print("\nAll 4 models + scaler saved!")
print(
    name,
    "Prediction:", 'pred',
    "Probabilities:",
    model.predict_proba(features)[0]
    if hasattr(model, "predict_proba")
    else "NO_PROBA"
)