import pandas as pd
import numpy as np
import re
import math
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# ----------------------------
# ENTROPY FUNCTION (ADVANCED FEATURE)
# ----------------------------
def entropy(url):
    p, lns = Counter(url), float(len(url))
    return -sum(count/lns * math.log2(count/lns) for count in p.values())


# ----------------------------
# FEATURE ENGINEERING
# ----------------------------
def extract_features(url):
    url = str(url)

    return [
        len(url),
        url.count("."),
        url.count("-"),
        url.count("@"),
        url.count("?"),
        url.count("&"),
        int("https" in url),
        int("http://" in url),
        int(bool(re.search(r"\d", url))),
        int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url))),  # IP address
        len(url.split("/")),
        len(url.split("/")[2].split(".")) if "://" in url else 0,  # subdomain depth
        int(any(word in url.lower() for word in ["login", "verify", "secure", "bank", "account"])),
        entropy(url)
    ]


# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("data/new_data_urls.csv")

df = df.dropna()
df = df.drop_duplicates()
df.columns = ["url", "label"]

# 🔥 ADD THIS (DATA SIZE CHECK + SPEED FIX)
print("Original dataset size:", df.shape)
df = df.sample(20000, random_state=42)
print("Sampled dataset size:", df.shape)

# ----------------------------
# FEATURES + LABELS
# ----------------------------
print("Starting feature extraction...")
X = np.array(df["url"].apply(extract_features).tolist())
print("Finished feature extraction")

y = df["label"]


# ----------------------------
# TRAIN / TEST SPLIT
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ----------------------------
# FEATURE SCALING (IMPORTANT FOR SVM + LOGISTIC REGRESSION)
# ----------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# ----------------------------
# MODELS
# ----------------------------
models = {
   "Logistic Regression": LogisticRegression(max_iter=100),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(),
    "SVM": SVC(kernel="linear")
}

# ----------------------------
# EVALUATION FUNCTION
# ----------------------------
def evaluate(model, name):
    preds = model.predict(X_test)

    return {
        "Model": name,
        "Accuracy": accuracy_score(y_test, preds),
        "Precision": precision_score(y_test, preds, zero_division=0),
        "Recall": recall_score(y_test, preds, zero_division=0),
        "F1 Score": f1_score(y_test, preds, zero_division=0)
    }


# ----------------------------
# TRAIN + EVALUATE ALL MODELS
# ----------------------------
results = []

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    print(f"Finished training {name}")
    results.append(evaluate(model, name))


# ----------------------------
# RESULTS TABLE
# ----------------------------
results_df = pd.DataFrame(results)
print("\nMODEL COMPARISON RESULTS:")
print(results_df)


# ----------------------------
# BEST MODEL
# ----------------------------
best_model = results_df.sort_values("F1 Score", ascending=False).iloc[0]

print("\nBEST MODEL:")
print(best_model)


# ----------------------------
# CONFUSION MATRIX (BEST MODEL)
# ----------------------------
best_model_name = best_model["Model"]
model = models[best_model_name]

preds = model.predict(X_test)
cm = confusion_matrix(y_test, preds)

print("\nCONFUSION MATRIX:")
print(cm)


# ----------------------------
# CLASS DISTRIBUTION CHECK
# ----------------------------
print("\nLABEL DISTRIBUTION:")
print(df["label"].value_counts())
# ----------------------------
# SAVE BEST MODEL
# ----------------------------
import joblib

joblib.dump(model, "phishing_model.pkl")
print("Model saved successfully!")