import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

// Components
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import Login from './components/Login';
import Registration from './components/Registration';
import NotFound from './components/NotFound';
import About from './components/About';
// import HeaderCalendar from './components/HeaderCalendar';
// import Fonts from './components/Fonts';

// Styles
import './App.css';

const App = () => {
  return (
    <Router>
      {/* <Fonts/> */}
      <Header />
      {/* <HeaderCalendar /> */}
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Registration />} />
          <Route path="/about" element={<About />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      {/* <Footer /> */}
    </Router>
  );
};

export default App;
