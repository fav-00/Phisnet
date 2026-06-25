import React from 'react';

function Navbar() {
  return (
    <header style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center', 
      borderBottom: '1px solid #1d2942', 
      paddingBottom: '20px',
      marginBottom: '20px'
    }}>
      <div className="system-title">
        <h1 style={{ fontSize: '24px', margin: '0 0 4px 0', color: '#fff', letterSpacing: '0.5px' }}>
          PHISHNET SYSTEM CONTROL PANEL
        </h1>
        <p style={{ fontSize: '13px', color: '#6e7d95', margin: '0' }}>
          Intelligent Client-Server Machine Learning Website Authentication Node
        </p>
      </div>
      <div className="system-meta-clock" style={{ display: 'flex', gap: '20px', fontSize: '13px', fontFamily: 'monospace', color: '#6e7d95' }}>
        <span>HOST NODE: LOCAL REPOSITORY [ACTIVE]</span>
        <span>PORT BOUND: 8000</span>
      </div>
    </header>
  );
}

export default Navbar;
