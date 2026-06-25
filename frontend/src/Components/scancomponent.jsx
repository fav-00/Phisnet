import React, { useState } from 'react';

function ScanComponent({ onScan, loading }) {
  const [inputUrl, setInputUrl] = useState('');

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (inputUrl.trim()) {
      onScan(inputUrl.trim());
    }
  };

  return (
    <section className="system-panel-card" style={{ backgroundColor: '#12192c', border: '1px solid #1d2942', borderRadius: '8px', padding: '24px', marginBottom: '20px' }}>
      <h2 className="panel-section-title" style={{ fontSize: '14px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.75px', color: '#d1e8ff', margin: '0 0 6px 0' }}>
        1. System Ingestion & Scan Component
      </h2>
      <p className="panel-section-subtitle" style={{ fontSize: '12px', color: '#6e7d95', margin: '0 0 20px 0' }}>
        Submit a web URL string vector to pass through the 14-feature extraction pipeline.
      </p>
      <form onSubmit={handleFormSubmit} style={{ display: 'flex', gap: '15px', marginTop: '15px' }}>
        <input 
          type="text" 
          className="url-input-field"
          placeholder="https:// Enter unverified website path link to analyze..."
          value={inputUrl}
          onChange={(e) => setInputUrl(e.target.value)}
          disabled={loading}
          style={{ flex: 1, backgroundColor: '#0d1322', border: '1px solid #1d2942', borderRadius: '6px', padding: '14px 18px', color: '#fff', fontFamily: 'monospace', fontSize: '14px' }}
        />
        <button 
          type="submit" 
          className="scan-action-button" 
          disabled={loading}
          style={{ backgroundColor: '#0a84ff', color: '#fff', border: 'none', borderRadius: '6px', padding: '0 28px', fontSize: '14px', fontNavWeight: '700', cursor: 'pointer' }}
        >
          {loading ? 'EXTRACTING MATRICES...' : 'RUN SCAN FILTER'}
        </button>
      </form>
    </section>
  );
}

export default ScanComponent;
