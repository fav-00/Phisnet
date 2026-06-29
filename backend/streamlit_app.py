import streamlit as st
import joblib
import math
import re
import numpy as np
import pandas as pd
import os
from datetime import datetime
from collections import Counter

# ==============================================================================
# 1. PAGE SETUP & NATIVE STYLING
# ==============================================================================
st.set_page_config(
    page_title="PhishNet Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .highlight-card-rf {
        border: 2px solid #0a84ff !important;
        background-color: rgba(10, 132, 255, 0.05) !important;
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FEATURE EXTRACTION ENGINE (38-Feature Matrix)
# ==============================================================================
def entropy(url):
    p, lns = Counter(url), float(len(url))
    return -sum(count/lns * math.log2(count/lns) for count in p.values())

def extract_features(url):
    url = str(url).lower()
    domain_split = url.split("://")[-1].split("/")
    domain = domain_split[0] if len(domain_split) > 0 else url
    return [
        len(url), len(domain), url.count("."), url.count("-"), url.count("@"),
        url.count("?"), url.count("&"), url.count("="), url.count("%"), url.count("_"),
        url.count(":"), url.count("#"), url.count("~"), url.count("/"),
        len(domain.split(".")) - 2 if len(domain.split(".")) > 2 else 0,
        len(domain.split(".")[-1]) if "." in domain else 0, domain.count("-"),
        sum(c.isdigit() for c in url), len(set(url)), entropy(url),
        int(url.startswith("https://")), int(url.startswith("http://")),
        int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url))), int(".." in url),
        int("//" in url[8:] if len(url) > 8 else False),
        int(any(s in url for s in ["bit.ly", "tinyurl", "t.co", "goo.gl"])),
        int(len(domain) > 30), int(len(url) > 75), int(len(url.split("/")) > 5),
        int("xn--" in domain),
        sum(word in url for word in ["login", "signin", "verify", "secure", "update", "account", "bank", "confirm", "password"]),
        int(any(b in url for b in ["paypal", "google", "amazon", "microsoft", "facebook", "apple"])),
        int(bool(re.search(r"(login|verify|secure|account).*\d", url))),
        int(domain.count("-") > 2), int(url.count(".") > 3),
        int(bool(re.search(r"[a-zA-Z]{10,}\d{3,}", url))),
        int(bool(re.search(r"free|bonus|gift|reward|claim", url))),
        int(bool(re.search(r"verify-account|secure-login|update-info", url)))
    ]

@st.cache_resource
def load_assets():
    base_dir = os.path.dirname(__file__) if "__file__" in locals() else "."
    if not os.path.basename(base_dir) == "backend" and os.path.exists("backend"):
        base_dir = os.path.join(base_dir, "backend")
    
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
    st.error(f"❌ Execution Fault: Backend pipeline artifacts missing. Error: {e}")
    st.stop()

if "scan_history" not in st.session_state:
    st.session_state.scan_history = None

# ==============================================================================
# 3. SIDEBAR NAVIGATION COMPONENT
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:25px;">
        <div style="background:#0a84ff; width:32px; height:32px; border-radius:6px; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#fff; font-family:sans-serif;">P</div>
        <span style="font-weight:bold; color:#fff; font-size:18px; letter-spacing:1px; font-family:sans-serif;">PHISHNET</span>
    </div>
    """, unsafe_allow_html=True)
    
    active_page = st.radio(
        "Navigation",
        options=["URL Scanner", "Model Analytics", "About PhishNet"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>" * 12, unsafe_allow_html=True)
    
    engine_color = "#30d158"
    if st.session_state.scan_history and st.session_state.scan_history["phishing_count"] >= 3:
        engine_color = "#ff453a"
        
    st.markdown(f"""
    <div style="border-top:1px solid #1d2942; padding-top:15px;">
        <div style="font-size:10px; color:#6e7d95; text-transform:uppercase; font-weight:bold; font-family:sans-serif;">Core Engine</div>
        <div style="display:flex; align-items:center; gap:8px; margin-top:6px;">
            <div style="width:8px; height:8px; border-radius:50%; background-color:{engine_color};"></div>
            <span style="font-size:12px; color:#fff; font-weight:bold; font-family:sans-serif;">v1.4.0 (4 Models Active)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. MAIN WORKSPACE TOP-BAR TELEMETRY AREA
# ==============================================================================
col_title, col_clock = st.columns([2, 1])
with col_title:
    st.markdown("""
    <div style="font-family:sans-serif;">
        <h1 style="margin:0; font-size:26px; font-weight:bold; color:#fff; letter-spacing:0.5px;">PHISHNET DASHBOARD</h1>
        <p style="margin:0; font-size:13px; color:#6e7d95;">Comparative ML Phishing Detection Platform</p>
    </div>
    """, unsafe_allow_html=True)

with col_clock:
    dynamic_today = datetime.now().strftime("%b %d, %Y").upper()
    st.markdown(f"""
    <div style="text-align:right; font-family:monospace; font-size:12px; color:#6e7d95; padding-top:10px; line-height:1.4;">
        <div>DATE: {dynamic_today}</div>
        <div>PORT: 8000 [ACTIVE]</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin:15px 0; border:0; border-top:1px solid #1d2942;'>", unsafe_allow_html=True)

# ==============================================================================
# 5. PAGE ROUTING CONTROLLER
# ==============================================================================
if active_page == "URL Scanner":
    if st.session_state.scan_history is None:
        st.info("🟢 SYSTEM STATUS: OPERATIONAL")
    elif st.session_state.scan_history["phishing_count"] >= 3:
        st.error("🔴 SYSTEM STATUS: SECURED (THREAT CONTEXT ISOLATED)")
    else:
        st.success("🟢 SYSTEM STATUS: RUNNING (SAFE LINK MONITORED)")
        
    st.write("")
    
    st.markdown("### System Ingestion & Scan Component")
    st.caption("Submit URL → Get predictions from all 4 ML models simultaneously")
    
    url_input = st.text_input("URL Vector String Ingestion Target:", placeholder="https:// Enter suspicious URL...", label_visibility="collapsed")
    
    if st.button("RUN COMPARE SCAN", type="primary", use_container_width=True):
        if not url_input.strip():
            st.warning("⚠️ Input vector field cannot be blank.")
        else:
            with st.spinner("PROCESSING DATA VECTORS / EXTRACTING 38 FEATURES..."):
                raw_feats = extract_features(url_input)
                scaled_feats = scaler.transform([raw_feats])
                
                computed_results = []
                phishing_count = 0
                
                for name, model in models.items():
                    pred = int(model.predict(scaled_feats)[0])
                    
                    if hasattr(model, "predict_proba"):
                        raw_proba = float(model.predict_proba(scaled_feats)[0][1])
                        confidence_val = raw_proba if pred == 1 else (1 - raw_proba)
                        confidence_str = f"{confidence_val * 100:.1f}%"
                    else:
                        confidence_str = "N/A (Decision Boundary Based)"
                        
                    if pred == 1:
                        phishing_count += 1
                        
                    computed_results.append({
                        "model": name,
                        "prediction": pred,
                        "label": "🚨 PHISHING THREAT DETECTED" if pred == 1 else "✅ LEGITIMATE ACCESS VERIFIED",
                        "confidence": confidence_str
                    })
                
                st.session_state.scan_history = {
                    "url": url_input,
                    "phishing_count": phishing_count,
                    "results": computed_results
                }
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Real-Time Model Comparison Results")
    st.caption("All 4 models voting on this URL")
    
    if st.session_state.scan_history is None:
        st.markdown("""
        <div style="background:#1c1c1e; border:1px dashed #1d2942; border-radius:6px; padding:35px; text-align:center; color:#6e7d95; font-size:13px; font-family:sans-serif;">
            No scan performed yet. Submit a URL above to see RF, GB, LR, and SVM metrics.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.text(f"Scanned Target Vector: {st.session_state.scan_history['url']}")
        grid_col1, grid_col2 = st.columns(2)
        
        for index, item in enumerate(st.session_state.scan_history["results"]):
            target_column = grid_col1 if index % 2 == 0 else grid_col2
            
            if item["prediction"] == 1:
                target_column.error(f"{item['model'].upper()}  \n{item['label']} | Confidence: {item['confidence']}")
            else:
                target_column.success(f"{item['model'].upper()}  \n{item['label']} | Confidence: {item['confidence']}")
elif active_page == "Model Analytics":
    st.markdown("### Model Benchmarking Analytics & Evaluation Matrix")
    st.caption("Performance telemetry derived from cross-validation scripts")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Random Forest Accuracy", value="94.41%", delta="Primary Model")
    m2.metric(label="Gradient Boosting Accuracy", value="90.30%")
    m3.metric(label="SVM Accuracy", value="83.39%")
    m4.metric(label="Logistic Regression Accuracy", value="83.54%")
    st.markdown("", unsafe_allow_html=True)
    col_table, col_chart = st.columns([4, 3])
    with col_table:
        st.markdown("##### Performance Matrix Records")
        metrics_dict = {
            "Model Architecture": ["Random Forest", "Gradient Boosting", "Support Vector Machine (SVM)", "Logistic Regression"],
            "Accuracy": ["94.41%", "90.30%", "83.39%", "83.54%"],
            "Precision": ["94.02%", "89.28%", "83.57%", "83.99%"],
            "Recall": ["95.49%", "92.80%", "85.34%", "85.07%"],
            "F1-Score": ["94.75%", "91.00%", "84.45%", "84.53%"]
        }
        st.dataframe(pd.DataFrame(metrics_dict), use_container_width=True, hide_index=True)
        st.caption("💡 Highlight: Random Forest achieved highest structural data validation accuracy scores.")
    with col_chart:
        st.markdown("##### Accuracy Visual Comparison")
        chart_data = pd.DataFrame({
            'Model': ['Random Forest', 'Gradient Boosting', 'Logistic Reg.', 'SVM'],
            'Accuracy (%)': [94.41, 90.30, 83.54, 83.39]
        })
        st.bar_chart(chart_data, x='Model', y='Accuracy (%)', color="#0a84ff", use_container_width=True)
elif active_page == "About PhishNet":
    st.markdown("### About the PhishNet Architecture Framework")
    st.caption("Technical thesis specifications overview")
    st.info("""
        PhishNet is an intelligent cybersecurity application built for comparative real-time URL risk evaluation.
        By leveraging a balanced lexical dataset, the system extracts a precise 38-feature structural vector to evaluate URL integrity without accessing live webpage scripts or risking execution payloads.
    """)
    left_spec, right_spec = st.columns(2)
    with left_spec:
        st.markdown("""
            ##### Framework Architecture Specs
            *   Ingestion Pipeline: 38 Lexical, Host-Based, and Behavioral Features
            *   Core Backend Port: 8000 (FastAPI Pipeline Router)
            *   State Control System: Native Single-Thread Operational Rendering
            *   Data Footprint Base: 808,042 Cleaned Training Records
        """)
    with right_spec:
        st.markdown("""
            ##### Ensemble Design Goals
            *   Zero-Day Protection: Mitigate domain spoofing vectors efficiently.
            *   Low Latency: Lower high processing latency over content analysis approaches.
            *   Paradigms: Evaluate comparative variance across different structural model configurations.
        """)
    st.markdown("***")


