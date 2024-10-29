// Logo.js
import React from 'react';

const Logo = () => {
  return (
    <div style={styles.logoContainer}>
      <span style={styles.text}>LIQAA</span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        style={styles.icon}
      >
        <path d="M12 1v10a4 4 0 0 1-8 0V1" />
        <path d="M5 10v11a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V10" />
      </svg>
    </div>
  );
};

const styles = {
  logoContainer: {
    display: 'flex',
    alignItems: 'center',
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#4CAF50', // Change the color as needed
    textDecoration: 'none',
  },
  text: {
    marginRight: '8px', // Space between text and icon
    textDecoration: 'none',
  },
  icon: {
    width: '1em',
    height: '1em',
  },
};

export default Logo;
