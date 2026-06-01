import React from 'react';
import { Link } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <Link to="/" className="logo">Hobbyist AI</Link>
        <div className="nav-links">
          <Link to="/get-started">Get Started</Link>
          <Link to="/dashboard">Dashboard</Link>
        </div>
      </nav>

      <main>
        {/* Will render route components here */}
      </main>

      <footer className="footer">
        <p>© 2024 Hobbyist AI - AI-Powered Hobby Recommendations</p>
      </footer>
    </div>
  );
}

export default App;