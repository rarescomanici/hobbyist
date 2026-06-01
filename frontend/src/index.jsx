import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import GetStarted from './pages/GetStarted';
import InterestForm from './pages/InterestForm';
import HobbyDashboard from './pages/HobbyDashboard';
import API from './api';

function HomePage() {
  return (
    <div>
      <h1>Welcome to Hobbyist AI</h1>
      <p>Your personalized hobby recommendation engine powered by AI.</p>
      <br />
      <button onClick={() => window.location.href = '/get-started'}>
        Get Started
      </button>
    </div>
  );
}

function NotFound() {
  return (
    <div>
      <h1>404 - Page Not Found</h1>
      <Link to="/">Go Home</Link>
    </div>
  );
}

function Layout({ children }) {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<HomePage />} />
          <Route path="get-started" element={<GetStarted />} />
          <Route path="interest-form" element={<InterestForm API={API} />} />
          <Route path="dashboard" element={<HobbyDashboard API={API} />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default Layout;