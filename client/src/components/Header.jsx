// Header.js
import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <div className={styles.circle}></div>
        <Link to="/home" className={styles.brandName}>
          LIQAA
        </Link>{' '}
        {/* Brand name is now a link */}
      </div>
      <nav className={styles.navLinks}>
        <Link to="/home">Home</Link>
        <Link to="/pricing">Pricing</Link>
        <Link to="/support">Support</Link>
        <Link to="/about">About Us</Link>
      </nav>
      <div className={styles.signupButton}>
        <button>Sign Up</button>
      </div>
    </header>
  );
};

export default Header;
