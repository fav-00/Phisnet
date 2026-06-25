import streamlit as st
import joblib
import math
import re
import numpy as np
import pandas as pd
import os
from collections import Counter

# 1. Page Settings
st.set_page_config(
    page_title="PhisNet - Phishing Detection System",
    page_icon="🛡️",
    layout="wide"
)

# 2. Entropy and Feature Extraction (Fixed Domain Bug)
def entropy(url):
    p, lns = Counter(url), float(len(url))
    return -sum(count/lns * math.log2(count/lns) for count in p.values())

def extract_features(url):
    url = str(url).lower()
    domain_split = url.split("://")[-1].split("/")
    # FIXED: Extracting index 0 properly so domain remains a string
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
        int(any(s in url for s in ["bit.ly", "tinyurl", "t.co", "goo.gl"])),
        int(len(domain) > 30),
        int(len(url) > 75),
        int(len(url.split("/")) > 5),
        int("xn--" in domain),
        sum(word in url for word in ["login", "signin", "verify", "secure", "update", "account", "bank", "confirm", "password"]),
        int(any(b in url for b in ["paypal", "google", "amazon", "microsoft", "facebook", "apple"])),
        int(bool(re.search(r"(login|verify|secure|account).*\d", url))),
        int(domain.count("-") > 2),
        int(url.count(".") > 3),
        int(bool(re.search(r"[a-zA-Z]{10,}\d{3,}", url))),
        int(bool(re.search(r"free|bonus|gift|reward|claim", url))),
        int(bool(re.search(r"verify-account|secure-login|update-info", url)))
    ]

# 3. Cache the Models and Scaler (Handles paths when run from backend/)
@st.cache_resource
def load_assets():
    # Detect running directory to prevent FileNotFoundError on Streamlit Cloud
    base_dir = os.path.dirname(__file__) if "__file__" in locals() else "."
    
    models = {
        "Random Forest": joblib.load(os.path.join(base_dir, "rf_model.pkl")),
        "Gradient Boosting": joblib.load(os.path.join(base_dir, "gb_model.pkl")),
        "Logistic Regression": joblib.load(os.path.join(base_dir, "lr_model.pkl")),
        "SVM": joblib.load(os.path.join(base_dir, "svm_model.pkl"))
    }
    scaler = joblib.load(os.path.join(base_dir, "scaler.pkl"))
    return models, scaler

try:
    models, scaler = load_assets()
except Exception as e:
    st.error(f"❌ Error loading assets. Make sure your .pkl files are in the same folder as streamlit_app.py. Error: {e}")
    st.stop()

# 4. App UI Layout
st.title("🛡️ PhisNet: Multi-Model Phishing Detection")
st.write("Analyze URLs against your trained Machine Learning models to identify phishing indicators.")

# Tabs for separate features
tab1, tab2 = st.tabs(["🎯 Single Model Predictor", "📊 Multi-Model Comparison"])

with tab1:
    st.subheader("Analyze with a specific model")
    col1, col2 = st.columns(2)
    
    with col1:
        url_input = st.text_input("Enter URL to Test:", placeholder="http://example.com", key="single_url")
    with col2:
        selected_model = st.selectbox("Select Model", list(models.keys()))

    if st.button("Run Diagnostics", type="primary"):
        if not url_input.strip():
            st.warning("Please enter a URL first!")
        else:
            with st.spinner("Analyzing..."):
                raw_feats = extract_features(url_input)
                scaled_feats = scaler.transform([raw_feats])
                
                model = models[selected_model]
                pred = int(model.predict(scaled_feats)[0])
                
                proba = None
                if hasattr(model, "predict_proba"):
                    proba = float(model.predict_proba(scaled_feats)[0][1])
                
                st.write("### Analysis Verdict")
                if pred == 1:
                    st.error(f"🚨 **DANGER: This URL is classified as PHISHING by {selected_model}!**")
                else:
                    st.success(f"✅ **SAFE: This URL is classified as LEGITIMATE by {selected_model}.**")
                
                if proba is not None:
                    confidence = proba if pred == 1 else (1 - proba)
                    st.metric(label="Model Confidence", value=f"{confidence * 100:.2f}%")
                else:
                    st.info("💡 Note: Probability score is unavailable for this specific model (e.g., Linear SVM).")

with tab2:
    st.subheader("Compare Predictions Across All Models")
    comp_url = st.text_input("Enter URL for Comparative Evaluation:", placeholder="http://example.com", key="comp_url")
    
    if st.button("Compare All Models", type="secondary"):
        if not comp_url.strip():
            st.warning("Please enter a URL first!")
        else:
            with st.spinner("Gathering model matrix records..."):
                raw_feats = extract_features(comp_url)
                scaled_feats = scaler.transform([raw_feats])
                
                summary_data = []
                for name, model in models.items():
                    pred = int(model.predict(scaled_feats)[0])
                    proba = float(model.predict_proba(scaled_feats)[0][1]) if hasattr(model, "predict_proba") else None
                    
                    confidence_str = f"{proba * 100:.2f}%" if proba is not None else "N/A"
                    if proba is not None and pred == 0:
                        confidence_str = f"{(1 - proba) * 100:.2f}%"
                        
                    summary_data.append({
                        "Model Classifier": name,
                        "Verdict": "🚨 Phishing" if pred == 1 else "✅ Legitimate",
                        "Confidence Level": confidence_str
                    })
                
                st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
