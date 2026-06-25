import React from 'react';

function ThreatPanel({ prediction, loading, error, scannedUrl }) {
  return (
    <section className="system-panel-card" style={{ backgroundColor: '#12192c', border: '1px solid #1d2942', borderRadius: '8px', padding: '24px', marginBottom: '20px' }}>
      <h2 className="panel-section-title" style={{ fontSize: '14px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.75px', color: '#d1e8ff', margin: '0 0 6px 0' }}>
        2. Real-Time Threat Classification & Alert Panel
      </h2>
      <p className="panel-section-subtitle" style={{ fontSize: '12px', color: '#6e7d95', margin: '0 0 20px 0' }}>
        Instant malware boundary classification and error diagnostics returned from the server gateway.
      </p>
      
      {/* CONDITIONAL RENDERING CONTROL BLOCKS */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '20px', color: '#ffd60a', fontFamily: 'monospace', fontSize: '13px', fontWeight: 'bold' }}>
          [PHISHNET ACTIVE] Extracting 13 Lexical Parameters + Calculating Shannon Entropy...
        </div>
      ) : error ? (
        <div style={{ background: 'rgba(255, 69, 58, 0.1)', border: '2px solid #ff453a', padding: '20px', borderRadius: '6px', color: '#ff453a', textAlign: 'center', fontFamily: 'monospace', fontWeight: 'bold' }}>
          {error}
        </div>
      ) : prediction === null ? (
        <div className="alert-placeholder-box" style={{ border: '1px dashed #1d2942', borderRadius: '6px', padding: '40px', textAlign: 'center', color: '#6e7d95', fontSize: '13px' }}>
          No scan performed yet. Submit a URL string above to view real-time threat alert results.
        </div>
      ) : prediction === 1 ? (
        <div className="alert-output-banner danger" style={{ padding: '24px', borderRadius: '6px', textAlign: 'center', fontFamily: 'monospace', fontSize: '16px', fontWeight: 'bold', background: 'rgba(255, 69, 58, 0.1)', border: '2px solid #ff453a', color: '#ff453a' }}>
          <div style={{ fontSize: '11px', color: '#6e7d95', marginBottom: '6px', fontWeight: 'normal' }}>TARGET: {scannedUrl}</div>
          CRITICAL WARNING: ADVERSARIAL PHISHING THREAT DETECTED & SEGREGATED SUCCESSFULLY
        </div>
      ) : (
        <div className="alert-output-banner success" style={{ padding: '24px', borderRadius: '6px', textAlign: 'center', fontFamily: 'monospace', fontSize: '16px', fontWeight: 'bold', background: 'rgba(48, 209, 88, 0.1)', border: '2px solid #30d158', color: '#30d158' }}>
          <div style={{ fontSize: '11px', color: '#6e7d95', marginBottom: '6px', fontWeight: 'normal' }}>TARGET: {scannedUrl}</div>
          VERIFIED SECURE: AUTHENTICATED DOMAIN RESOURCE SPACE GRANTED CLEARED ACCESS
        </div>
      )}
    </section>
  );
}

export default ThreatPanel;
