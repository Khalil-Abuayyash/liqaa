import React from 'react';
import './HeaderCalendar.css';
import { Link } from 'react-router-dom';
import Logo from './Logo';

function Header() {
  return (
    <header className="header">
      <h1 className="logo">LIQAA</h1>
      <Link to="/home">
        <div className="calendar home-calendar">
          <div className="calendar-header">HOME</div>
          {/* <div className="calendar-days">
            <div className="day"></div>
            <div className="day">H</div>
            <div className="day">O</div>
            <div className="day">M</div>
            <div className="day">E</div>
            <div className="day"></div>
            <div className="day">P</div>
            <div className="day">A</div>
            <div className="day">G</div>
            <div className="day">E</div>
            <div className="day"></div>
            <div className="day"></div>
          </div> */}
        </div>
      </Link>

      <Link to="/about">
        <div className="calendar about-calendar">
          <div className="calendar-header">ABOUT</div>
          {/* <div className="calendar-days">
            <div className="day"></div>
            <div className="day"></div>
            <div className="day">A</div>
            <div className="day">B</div>
            <div className="day">O</div>
            <div className="day">U</div>
            <div className="day">T</div>
            <div className="day"></div>
            <div className="day"></div>
            <div className="day">U</div>
            <div className="day">S</div>
            <div className="day"></div>
          </div> */}
        </div>
      </Link>

      <Link to="/login">
        <div className="calendar login-calendar">
          <div className="calendar-header">LOG IN</div>
          {/* <div className="calendar-days">
            <div className="day"></div>
            <div className="day">L</div>
            <div className="day">O</div>
            <div className="day">G</div>
            <div className="day"></div>
            <div className="day">I</div>
            <div className="day">N</div>
            <div className="day"></div>
            <div className="day">O</div>
            <div className="day">U</div>
            <div className="day">T</div>
            <div className="day"></div>
          </div> */}
        </div>
      </Link>

      <Link to="/register">
        <div className="calendar register-calendar">
          <div className="calendar-header">REGISTER</div>
          {/* <div className="calendar-days">
            <div className="day"></div>
            <div className="day">R</div>
            <div className="day">E</div>
            <div className="day">G</div>
            <div className="day">I</div>
            <div className="day">S</div>
            <div className="day">T</div>
            <div className="day">E</div>
            <div className="day">R</div>
            <div className="day"></div>
            <div className="day"></div>
            <div className="day"></div>
          </div> */}
        </div>
      </Link>
    </header>
  );
}

export default Header;
