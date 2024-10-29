// About.js
import React from 'react';
import './About.css'; // Optional: Import a CSS file for styles

const About = () => {
  return (
    <div className="about-container">
      <h2>About This Application</h2>
      <p>
        Welcome to the Interview App! This platform is designed to connect users
        for interviews, providing a seamless way to schedule and conduct
        discussions on various topics. Whether you're preparing for a job
        interview, seeking mentorship, or just curious to explore new
        perspectives, our application aims to facilitate meaningful
        conversations.
      </p>
      <h3>Our Mission</h3>
      <p>
        Our mission is to make interview processes more accessible and engaging
        for everyone. We believe in the power of communication and knowledge
        sharing, and we strive to create a supportive environment for users to
        connect and learn from one another.
      </p>
      <h3>Features</h3>
      <ul>
        <li>User-friendly interface for scheduling interviews</li>
        <li>Secure login and registration</li>
        <li>Real-time notifications for upcoming interviews</li>
        <li>Profile management and user connections</li>
      </ul>
      <h3>Get in Touch</h3>
      <p>
        If you have any questions or feedback, feel free to reach out to us via
        the contact page. We are always here to help!
      </p>
    </div>
  );
};

export default About;
