// Card.js
import React from 'react';
import styles from './Card.module.css';
import { SiGotomeeting } from 'react-icons/si';

const Card = ({ title, content, icon }) => {
  return (
    <div className={styles.card}>
      <div className={styles.iconContainer}>
        <SiGotomeeting className={styles.icon} />
      </div>
      <div className={styles.cardContent}>
        <h2 className={styles.cardTitle}>{title}</h2>
        <p>{content}</p>
      </div>
    </div>
  );
};

export default Card;
