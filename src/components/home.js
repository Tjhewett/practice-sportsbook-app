import React from 'react';
import logo from '../logo.svg';
import '../styles/home.css'

function Home() {
  return (
    <div className="home">
      <br />
        <h2>Gridiron Wager</h2>
        <h3>A Practice Betting Enviornment</h3>
      <header className="home-header">
        <img src={logo} className="home-logo" alt="logo" />
      </header>
      <br />
      <h3>Created By - Trevor Hewett</h3>
    </div>
  );
}

export default Home;