import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import AIChat from './components/AIChat';
import './App.css';

function App() {
  // Check authentication status synchronously on initial render
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return !!localStorage.getItem('user');
  });

  useEffect(() => {
    // Listen for custom events that indicate login/logout
    const handleAuthChange = () => {
      const user = localStorage.getItem('user');
      setIsLoggedIn(!!user);
    };

    // Listen for custom auth events
    window.addEventListener('authChange', handleAuthChange);

    return () => {
      window.removeEventListener('authChange', handleAuthChange);
    };
  }, []);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route 
            path="/chat" 
            element={isLoggedIn ? <AIChat /> : <Navigate to="/login" />} 
          />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
