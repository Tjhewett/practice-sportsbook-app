import React, { useState } from 'react';
import PlayerStats from '../sub-components/playerstats';
import TeamStats from '../sub-components/teamstats';
import NFLlogo from '../NFL-logo.png';
import '../styles/stats.css'


function StatPage() {
  const [currentView, setCurrentView] = useState('player');
  return (
    <div className="StatPage">
      <h2>Stats Page</h2>
      <div className='buttoncontainer'>
      <button onClick={() => setCurrentView('player')}>Player Stats</button>
      <button onClick={() => setCurrentView('team')}>Team Stats</button>

      {currentView === 'player' && <PlayerStats />}
      {currentView === 'team' && <TeamStats />}
      </div>
      <h4 className="stats-provider">Stats provided by: 
        <a href="https://www.nfl.com/stats/player-stats/">
            <img src={NFLlogo} alt="NFL Logo"/>
        </a>
      </h4>
    </div>
  );
}

export default StatPage;