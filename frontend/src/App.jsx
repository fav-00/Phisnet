import React, { useState } from 'react';
import Navbar from './Components/navbar';
import ScanComponent from './Components/scancomponent';
import ThreatPanel from './Components/threatpanel';
import BenchmarkPanel from './Components/benchmarkpanel';
import Footer from './Components/footer';
import './App.css';

function App() {
  const [scannedUrl, setScannedUrl] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const runSystemFilterPipeline = async (targetUrl) => {
    setScannedUrl(targetUrl);
    setLoading(true);
    setPrediction(null);
    setError('');

    try {
      // Direct numeric link payload transmission to your active FastAPI port
      const response = await fetch('http://127.0.0', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: targetUrl }),
      });

      if (!response.ok) {
        throw new Error('Server returned an internal execution exception.');
      }

      const result = await response.json();
      setPrediction(result.prediction);
    } catch (err) {
      console.error(err);
      setError('EXECUTION FAULT: Failed to connect to FastAPI API services. Confirm uvicorn server status.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-layout" style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#090e1a', color: '#f5f5f7' }}>
      
      {/* SIDEBAR SYSTEM PANEL NAVIGATION BAR */}
      <aside className="sidebar" style={{ width: '240px', backgroundColor: '#0b1120', borderRight: '1px solid #1d2942', padding: '25px 20px', display: 'flex', flexDirection: 'column', gap: '30px' }}>
        <div className="brand-area" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ backgroundColor: '#0a84ff', width: '32px', height: '32px', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: '#fff' }}>P</div>
          <span className="brand-logo" style={{ fontWeight: '900', fontSize: '20px', color: '#fff', letterSpacing: '1px' }}>PHISHNET</span>
        </div>
        <ul className="nav-links" style={{ display: 'flex', flexDirection: 'column', gap: '8px', listStyle: 'none', padding: 0, margin: 0 }}>
          <li className="nav-item active" style={{ padding: '12px 16px', borderRadius: '6px', color: '#0a84ff', backgroundColor: 'rgba(10, 132, 255, 0.15)', fontWeight: '600', fontSize: '14px' }}>Dashboard</li>
          <li className="nav-item" style={{ padding: '12px 16px', color: '#6e7d95', fontSize: '14px' }}>Scan History</li>
          <li className="nav-item" style={{ padding: '12px 16px', color: '#6e7d95', fontSize: '14px' }}>Model Analytics</li>
          <li className="nav-item" style={{ padding: '12px 16px', color: '#6e7d95', fontSize: '14px' }}>System Logs</li>
        </ul>
      </aside>

      {/* MAIN DATA FEED WORKSPACE FEED PANEL */}
      <main className="main-workspace" style={{ flex: 1, padding: '30px 40px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <Navbar />
        
        {/* COMPONENT 1 MOUNT: INGESTION INPUT CARD */}
        <ScanComponent onScan={runSystemFilterPipeline} loading={loading} />
        
        {/* COMPONENT 2 MOUNT: DYNAMIC ALERT RESPONSE BANNER */}
        <ThreatPanel prediction={prediction} loading={loading} error={error} scannedUrl={scannedUrl} />
        
        {/* COMPONENT 3 MOUNT: PERFORMANCE ANALYTICS PLATFORM */}
        <BenchmarkPanel />
        
        <Footer />
      </main>
      
    </div>
  );
}

export default App;
