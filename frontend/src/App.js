import React, { useState } from 'react';
import './App.css';

function App() {
  const [urlInput, setUrlInput] = useState('');
  const [results, setResults] = useState([]); // changed from single prediction
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('SYSTEM STATUS: OPERATIONAL');
  const [statusColor, setStatusColor] = useState('#30d158');
  const [activePage, setActivePage] = useState('dashboard');

  const executeScanFilter = async (e) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    setLoading(true);
    setResults([]);
    setStatusMessage('PROCESSING DATA VECTORS / EXTRACTING 38 FEATURES...');
    setStatusColor('#ffd60a');

    try {
      // CHANGED: hit /compare instead of /predict
      const response = await fetch('/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: urlInput.trim() }),
      });

      const data = await response.json();
      setResults(data.results || []);

      // Status based on majority vote
      const phishingCount = data.results.filter(r => r.prediction === 1).length;
      if (phishingCount >= 3) {
        setStatusMessage('SYSTEM STATUS: SECURED (THREAT CONTEXT ISOLATED)');
        setStatusColor('#ff453a');
      } else {
        setStatusMessage('SYSTEM STATUS: RUNNING (SAFE LINK MONITORED)');
        setStatusColor('#30d158');
      }
    } catch (error) {
      console.error('Fetch error:', error);
      setStatusMessage('EXECUTION FAULT: BACKEND API SERVICE UNREACHABLE');
      setStatusColor('#ff453a');
      alert('TypeError: Failed to fetch. Ensure uvicorn server is active on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="brand-area">
          <div style={{ background: '#0a84ff', width: '32px', height: '32px', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: '#fff' }}>P</div>
          <span className="brand-logo">PHISHNET</span>
        </div>
        <ul className="nav-links">
          <li
            className={`nav-item ${activePage === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActivePage('dashboard')}
          >
            URL Scanner
          </li>

          <li
            className={`nav-item ${activePage === 'analytics' ? 'active' : ''}`}
            onClick={() => setActivePage('analytics')}
          >
            Model Analytics
          </li>

          <li
            className={`nav-item ${activePage === 'about' ? 'active' : ''}`}
            onClick={() => setActivePage('about')}
          >
            About PhishNet
          </li>
        </ul>
        <div style={{ marginTop: 'auto', borderTop: '1px solid #1d2942', paddingTop: '15px' }}>
          <div style={{ fontSize: '10px', color: '#6e7d95', textTransform: 'uppercase', fontWeight: 'bold' }}>Core Engine</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '6px' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: statusColor }}></div>
            <span style={{ fontSize: '12px', color: '#fff', fontWeight: 'bold' }}>v1.4.0 (4 Models Active)</span>
          </div>
        </div>
      </aside>

      <main className="main-workspace">
        <div className="top-bar">
          <div className="system-title">
            <h1>PHISHNET DASHBOARD</h1>
            <p>Comparative ML Phishing Detection Platform</p>
          </div>
          <div className="system-meta-clock">
            <span>DATE: JUN 18, 2026</span>
            <span>PORT: 8000 [ACTIVE]</span>
          </div>
        </div>

        <section className="system-panel-card">
          <h2 className="panel-section-title">System Ingestion & Scan Component</h2>
          <p className="panel-section-subtitle">Submit URL → Get predictions from all 4 ML models</p>
          <form onSubmit={executeScanFilter} className="search-bar-wrapper">
            <input 
              type="text" 
              className="url-input-field"
              placeholder="https:// Enter suspicious URL..."
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" className="scan-action-button" disabled={loading}>
              {loading ? 'EXTRACTING MATRICES...' : 'RUN COMPARE SCAN'}
            </button>
          </form>
        </section>

        {/* NEW: Show all 4 model results */}
        <section className="system-panel-card">
          <h2 className="panel-section-title">Real-Time Model Comparison Results</h2>
          <p className="panel-section-subtitle">All 4 models voting on this URL</p>
          
          {results.length === 0 ? (
            <div className="alert-placeholder-box">
              <span>No scan performed yet. Submit a URL above to see RF, GB, LR, SVM predictions.</span>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
              {results.map((r, idx) => (
                <div key={idx} className={`alert-output-banner ${r.prediction === 1 ? 'danger' : 'success'}`}>
                  <div style={{ fontWeight: 'bold', fontSize: '12px' }}>{r.model.toUpperCase()}</div>
                  <div style={{ fontSize: '10px', marginTop: '4px' }}>
                    {r.label} | Confidence: {(r.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Your existing metrics table - keep it, but load from /metrics later */}
        <section className="system-panel-card">
          <h2 className="panel-section-title">Model Benchmarking Analytics & Evaluation Matrix</h2>
          <p className="panel-section-subtitle">Performance from model_metrics.csv</p>
          
          <div className="analytics-metrics-display">
  <div className="metric-mini-box"><div className="title">RF Accuracy</div><div className="value" style={{ color: '#0a84ff' }}>94.41%</div></div>
  <div className="metric-mini-box"><div className="title">GB Accuracy</div><div className="value" style={{ color: '#30d158' }}>90.30%</div></div>
  <div className="metric-mini-box"><div className="title">SVM Accuracy</div><div className="value" style={{ color: '#bf5af2' }}>83.39%</div></div>
  <div className="metric-mini-box"><div className="title">LR Accuracy</div><div className="value" style={{ color: '#ffd60a' }}>83.54%</div></div>
</div>

          <div className="analytics-grid-split">
            <div style={{ borderRight: '1px solid #1d2942', paddingRight: '20px' }}>
              <table className="matrix-evaluation-table">
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Accuracy</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1-Score</th>
                  </tr>
                </thead>
                <tbody>
  <tr className="highlight-rf-row">
    <td>Random Forest</td>
    <td>94.41%</td>
    <td>94.02%</td>
    <td>95.49%</td>
    <td>94.75%</td>
  </tr>
  <tr>
    <td>Gradient Boosting</td>
    <td>90.30%</td>
    <td>89.28%</td>
    <td>92.80%</td>
    <td>91.00%</td>
  </tr>
  <tr>
    <td>SVM</td>
    <td>83.39%</td>
    <td>83.57%</td>
    <td>85.34%</td>
    <td>84.45%</td>
  </tr>
  <tr>
    <td>Logistic Regression</td>
    <td>83.54%</td>
    <td>83.99%</td>
    <td>85.07%</td>
    <td>84.53%</td>
  </tr>
</tbody>
              </table>
            </div>

            <div className="visual-bar-chart-container">
              <div style={{ fontSize: '11px', color: '#6e7d95', fontWeight: 'bold', textTransform: 'uppercase' }}>Accuracy Visual Comparison</div>
              
              <div className="chart-bars-flex">
  <div className="bar-column-wrapper">
    <div style={{ fontSize: '10px', color: '#0a84ff', fontWeight: 'bold' }}>94.4%</div>
    <div className="bar-fill-track" style={{ height: '151px', backgroundColor: '#0a84ff' }}></div>
    <span className="bar-label-text">RF</span>
  </div>

  <div className="bar-column-wrapper">
    <div style={{ fontSize: '10px', color: '#30d158', fontWeight: 'bold' }}>90.3%</div>
    <div className="bar-fill-track" style={{ height: '144px', backgroundColor: '#30d158' }}></div>
    <span className="bar-label-text">GB</span>
  </div>

  <div className="bar-column-wrapper">
    <div style={{ fontSize: '10px', color: '#bf5af2', fontWeight: 'bold' }}>83.4%</div>
    <div className="bar-fill-track" style={{ height: '133px', backgroundColor: '#bf5af2' }}></div>
    <span className="bar-label-text">SVM</span>
  </div>

  <div className="bar-column-wrapper">
    <div style={{ fontSize: '10px', color: '#ffd60a', fontWeight: 'bold' }}>83.5%</div>
    <div className="bar-fill-track" style={{ height: '134px', backgroundColor: '#ffd60a' }}></div>
    <span className="bar-label-text">LR</span>
  </div>
              </div>
            </div>
          </div>
        </section>

        <footer style={{ marginTop: 'auto', display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: '#6e7d95', borderTop: '1px solid #1d2942', paddingTop: '15px' }}>
          <span>{statusMessage}</span>
          <span style={{ marginLeft: 'auto' }}>© 2026 PhishNet Platform. CCCS Bowen University.</span>
        </footer>
      </main>
    </div>
  );
}

export default App;