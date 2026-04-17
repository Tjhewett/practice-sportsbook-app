import React, { useState } from 'react';
import BetsforDraft from '../sub-components/betsfordraft';
import BetsforWeek1 from '../sub-components/betsforweek1';
import Betsforsuperbowl from '../sub-components/betsforsuperbowl';
import DKSBLogo from '../dksbIMG.png';
import '../styles/bets.css'

function BetPage() {
  const [currentView, setCurrentView] = useState('draft');
  return (
    <div className="BetPage">
      <h2>Bet Page</h2>
      <div className='buttoncontainer'>
      <button onClick={() => setCurrentView('draft')}>Draft Bets</button>
      <button onClick={() => setCurrentView('week1')}>Week1 Bets</button>
      <button onClick={() => setCurrentView('superbowl')}>SuperBowl Bets</button>
      {currentView === 'draft' && <BetsforDraft />}
      {currentView === 'week1' && <BetsforWeek1 />}
      {currentView === 'superbowl' && <Betsforsuperbowl />}
      </div>
      <h4 className="stats-provider">Odds provided by: 
        <a href="https://sportsbook.draftkings.com/leagues/football/nfl">
            <img src={DKSBLogo} alt="DKSB Logo"/>
        </a>
      </h4>
    </div>
  );
}

export default BetPage;