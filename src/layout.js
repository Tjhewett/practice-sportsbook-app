// Contains Browser Router to switch between components
import React, { useEffect, useState } from 'react';
import { Link, Route, Routes, BrowserRouter as Router, useNavigate} from 'react-router-dom';
import Home from './components/home';
import SignUp from './components/signup';
import SignIn from './components/signin';
import Stats from './components/stats';
import BetPage from './components/bets';
import ProtectedRoute from './components/protectedRoutes';
import AccountPage from './components/account';
import MiniGame from './components/minigame';
import './styles/layout.css';


const Navigation = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('token') !== null);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  }

  useEffect(() => {
    const is_auth_timer = setInterval(() => {
      setIsAuthenticated(localStorage.getItem('token') !== null);
    }, 1000);
    
    return () => clearInterval(is_auth_timer);
  }, []);
  return (
    <nav className="BigNav">
      <ul>
        <li><Link to="/">Home</Link></li>
        {!isAuthenticated && <li><Link to="/signup">Sign Up</Link></li>}
        {!isAuthenticated && <li><Link to="/signin">Sign In</Link></li>}
        <li><Link to="/stats">Stats</Link></li>
        {isAuthenticated && <li><Link to="/bets">Bets</Link></li>}
        {isAuthenticated && <li><Link to="/account">Account</Link></li>}
        {isAuthenticated && <li><Link to="/minigame">MiniGame</Link></li>}
        {isAuthenticated && <LogoutButton onLogout={handleLogout} />}
      </ul>
    </nav>
  );
};

const LogoutButton = ({ onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout(); 
    navigate('/'); // Navigate after logout
  };

  return (
    <li style={{ cursor: 'pointer' }} onClick={handleLogout}>Logout</li>
  );
};

const Layout = () => {
  return (
    <Router>
      <div>
        <Navigation />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/stats" element={<Stats />} />
            <Route path="/bets" element={<ProtectedRoute><BetPage /></ProtectedRoute>} />
            <Route path="/account" element={<ProtectedRoute><AccountPage /></ProtectedRoute>} />
            <Route path="/minigame" element={<ProtectedRoute><MiniGame /></ProtectedRoute>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default Layout;

