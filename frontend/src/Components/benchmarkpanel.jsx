import React from 'react';

function BenchmarkPanel() {
  return (
    <section className="system-panel-card" style={{ backgroundColor: '#12192c', border: '1px solid #1d2942', borderRadius: '8px', padding: '24px', marginTop: '20px' }}>
      {/* 3. MODEL BENCHMARKING ANALYTICS HEADER */}
      <h2 className="panel-section-title" style={{ fontSize: '14px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.75px', color: '#d1e8ff', margin: '0 0 6px 0' }}>
        3. Model Benchmarking Analytics & Evaluation Matrix
      </h2>
      <p className="panel-section-subtitle" style={{ fontSize: '12px', color: '#6e7d95', margin: '0 0 20px 0' }}>
        Performance comparison of machine learning models based on extensive testing and validation.
      </p>
      
      {/* FOUR ACCURACY CORE BOXES DISPLAY LAYOUT */}
      <div className="analytics-metrics-display" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', marginBottom: '25px' }}>
        <div className="metric-mini-box" style={{ backgroundColor: '#0d1322', border: '1px solid #1d2942', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
          <div className="title" style={{ fontSize: '11px', fontWeight: 'bold', color: '#6e7d95', textTransform: 'uppercase' }}>Accuracy</div>
          <div className="value" style={{ fontSize: '22px', fontWeight: '700', marginTop: '6px', color: '#0a84ff' }}>87.90%</div>
          <div style={{ fontSize: '10px', color: '#6e7d95', marginTop: '4px' }}>± 1.23%</div>
        </div>
        <div className="metric-mini-box" style={{ backgroundColor: '#0d1322', border: '1px solid #1d2942', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
          <div className="title" style={{ fontSize: '11px', fontWeight: 'bold', color: '#6e7d95', textTransform: 'uppercase' }}>Precision</div>
          <div className="value" style={{ fontSize: '22px', fontWeight: '700', marginTop: '6px', color: '#ffd60a' }}>87.43%</div>
          <div style={{ fontSize: '10px', color: '#6e7d95', marginTop: '4px' }}>± 1.45%</div>
        </div>
        <div className="metric-mini-box" style={{ backgroundColor: '#0d1322', border: '1px solid #1d2942', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
          <div className="title" style={{ fontSize: '11px', fontWeight: 'bold', color: '#6e7d95', textTransform: 'uppercase' }}>Recall</div>
          <div className="value" style={{ fontSize: '22px', fontWeight: '700', marginTop: '6px', color: '#bf5af2' }}>90.15%</div>
          <div style={{ fontSize: '10px', color: '#6e7d95', marginTop: '4px' }}>± 1.32%</div>
        </div>
        <div className="metric-mini-box" style={{ backgroundColor: '#0d1322', border: '1px solid #1d2942', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
          <div className="title" style={{ fontSize: '11px', fontWeight: 'bold', color: '#6e7d95', textTransform: 'uppercase' }}>F1-Score</div>
          <div className="value" style={{ fontSize: '22px', fontWeight: '700', marginTop: '6px', color: '#30d158' }}>88.77%</div>
          <div style={{ fontSize: '10px', color: '#6e7d95', marginTop: '4px' }}>± 1.15%</div>
        </div>
      </div>

      {/* GRID DIVISION SPLIT: DATA MATRIX TABLE VS ACCURACY COLUMN BAR GRAPH */}
      <div className="analytics-grid-split" style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '24px' }}>
        
        {/* COMPREHENSIVE EXPERIMENTAL EMPIRICAL RESULTS DATA TABLE */}
        <div style={{ borderRight: '1px solid #1d2942', paddingRight: '20px' }}>
          <table className="matrix-evaluation-table" style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', textAlign: 'left' }}>
            <thead>
              <tr style={{ color: '#6e7d95', borderBottom: '2px solid #1d2942' }}>
                <th style={{ padding: '10px' }}>Model Architecture Type</th>
                <th style={{ padding: '10px' }}>Accuracy</th>
                <th style={{ padding: '10px' }}>Precision</th>
                <th style={{ padding: '10px' }}>Recall</th>
                <th style={{ padding: '10px' }}>F1-Score</th>
              </tr>
            </thead>
            <tbody>
              <tr className="highlight-rf-row" style={{ fontWeight: 'bold', backgroundColor: 'rgba(10, 132, 255, 0.08)', color: '#fff' }}>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>Gini Random Forest (Selected) ⭐</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>87.90%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>87.43%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>90.15%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>88.77%</td>
              </tr>
              <tr style={{ color: '#e5e5ea' }}>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>Gradient Boosting (GBDT)</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>87.33%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>84.55%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>93.12%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>88.62%</td>
              </tr>
              <tr style={{ color: '#e5e5ea' }}>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>Linear Support Vector Classifier</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>81.00%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>78.68%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>88.02%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>83.09%</td>
              </tr>
              <tr style={{ color: '#e5e5ea' }}>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>L2 Logistic Regression</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>80.70%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>78.89%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>86.85%</td>
                <td style={{ padding: '10px', borderBottom: '1px solid #1d2942' }}>82.68%</td>
              </tr>
            </tbody>
          </table>
          <div style={{ marginTop: '15px', padding: '12px', background: 'rgba(10, 132, 255, 0.05)', borderLeft: '3px solid #0a84ff', borderRadius: '4px' }}>
            <div style={{ fontSize: '11px', fontWeight: 'bold', color: '#0a84ff', textTransform: 'uppercase' }}>Why Random Forest?</div>
            <p style={{ fontSize: '11px', color: '#6e7d95', margin: '4px 0 0 0', lineHeight: '1.4' }}>
              Random Forest achieved the optimal mathematical balance across your 14 features, providing high generalization accuracy and exceptional resilience on historical validation rows.
            </p>
          </div>
        </div>

        {/* CUSTOM LAYOUT MICRO ACCURACY COLUMN BAR GRAPH PANEL */}
        <div className="visual-bar-chart-container" style={{ backgroundColor: '#0d1322', border: '1px solid #1d2942', borderRadius: '6px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '220px' }}>
          <div style={{ fontSize: '11px', color: '#6e7d95', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Accuracy Visual Comparison</div>
          <div className="chart-bars-flex" style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'flex-end', height: '160px', paddingBottom: '10px' }}>
            <div className="bar-column-wrapper" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', width: '50px' }}>
              <div style={{ fontSize: '10px', color: '#0a84ff', fontWeight: 'bold' }}>87.9%</div>
              <div className="bar-fill-track" style={{ width: '24px', height: '135px', backgroundColor: '#0a84ff', borderRadius: '3px 3px 0 0' }}></div>
              <span className="bar-label-text" style={{ fontSize: '10px', color: '#6e7d95' }}>R-Forest</span>
            </div>
            <div className="bar-column-wrapper" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', width: '50px' }}>
              <div style={{ fontSize: '10px', color: '#30d158', fontWeight: 'bold' }}>87.3%</div>
              <div className="bar-fill-track" style={{ width: '24px', height: '130px', backgroundColor: '#30d158', borderRadius: '3px 3px 0 0' }}></div>
              <span className="bar-label-text" style={{ fontSize: '10px', color: '#6e7d95' }}>G-Boost</span>
            </div>
            <div className="bar-column-wrapper" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', width: '50px' }}>
              <div style={{ fontSize: '10px', color: '#bf5af2', fontWeight: 'bold' }}>81.0%</div>
              <div className="bar-fill-track" style={{ width: '24px', height: '110px', backgroundColor: '#bf5af2', borderRadius: '3px 3px 0 0' }}></div>
              <span className="bar-label-text" style={{ fontSize: '10px', color: '#6e7d95' }}>SVM</span>
            </div>
            <div className="bar-column-wrapper" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', width: '50px' }}>
              <div style={{ fontSize: '10px', color: '#ffd60a', fontWeight: 'bold' }}>80.7%</div>
              <div className="bar-fill-track" style={{ width: '24px', height: '105px', backgroundColor: '#ffd60a', borderRadius: '3px 3px 0 0' }}></div>
              <span className="bar-label-text" style={{ fontSize: '10px', color: '#6e7d95' }}>Log-Reg</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default BenchmarkPanel;
