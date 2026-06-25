import React from 'react';

function Footer() {
  return (
    <footer style={{ 
      marginTop: '40px', 
      display: 'flex', 
      justifyContent: 'space-between', 
      fontSize: '11px', 
      color: '#6e7d95', 
      borderTop: '1px solid #1d2942', 
      paddingTop: '15px' 
    }}>
      <span style={{ fontFamily: 'monospace' }}>
        SYSTEM ENGINE STATE: STANDBY (WAITING FOR USER STRING ENTRY INPUT)
      </span>
      <span>
        © 2026 PhishNet Detection Engine. CCCS Bowen University. All Rights Reserved.
      </span>
    </footer>
  );
}

export default Footer;
