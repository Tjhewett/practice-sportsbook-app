import React, { useEffect, useState } from 'react';
import '../styles/betsforsuperbowl.css'; 

const Betsforsuperbowl = () => {
    const [superbowlOdds, setsuperbowlOdds] = useState([]);
    const [userCurrency, setUserCurrency] = useState(0);
    const [betAmounts, setBetAmounts] = useState({});
  
    useEffect(() => {
      // Fetch user's currency from the API
      const fetchUserCurrency = async () => {
          try {
            const response = await fetch('http://127.0.0.1:5000/api/account', {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
              },
            });
            if (!response.ok) throw new Error('Failed to fetch user currency');
            const data = await response.json();
            setUserCurrency(data.currency);
          } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
          }
      };
  
      // Fetch the superbowl odds from the API
      const fetchsuperbowlOdds = async () => {
        try {
          const response = await fetch('http://127.0.0.1:5000/api/superbowl_odds');
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          setsuperbowlOdds(data);
        } catch (error) {
          console.error('There was an error fetching the week 1 odds:', error);
        }
      };
  
      fetchUserCurrency();
      fetchsuperbowlOdds();
    }, []);
  
    const handleBetAmountChange = (Team, amount) => {
      setBetAmounts(prev => ({ ...prev, [Team]: amount }));
    };
  
    const submitBet = async (Team, amount, odds) => {
      // Ensure that the bet amount is a number and is positive
      amount = parseFloat(amount);
      if (isNaN(amount) || amount <= 0 || amount > userCurrency) {
        alert('Please enter a valid bet amount within your currency limits.');
        return;
      }
  
      try {
        const response = await fetch('http://127.0.0.1:5000/api/place_bet_superbowl', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            Team: Team,
            odds: odds,
            amount: amount
          })
        });
  
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        setUserCurrency(data.newCurrency); // Update user currency
        setBetAmounts(prev => ({ ...prev, [Team]: '' }));
      } catch (error) {
        console.error('Error placing bet:', error);
        alert('There was an error placing your bet.');
      }
    };
  
    return (
        <div className="superbowl-bets-container">
          <h2>2025 Super Bowl Odds</h2>
          <div>Your Currency: ${userCurrency}</div>
          {superbowlOdds.map((odd) => (
            <div key={odd.Team} className="bet-item">
              <span>{odd.Team}</span>
              <input
                type="number"
                value={betAmounts[odd.Team] || ''}
                onChange={(e) => handleBetAmountChange(odd.Team, e.target.value)}
                placeholder="Bet Amount"
                min="1"
                max={userCurrency}
              />
              <button className="btn-main" onClick={() => submitBet(odd.Team, betAmounts[odd.Team], odd.odds)}>{odd.odds}</button>
            </div>
          ))}
        </div>
      );
  };
  
  export default Betsforsuperbowl;