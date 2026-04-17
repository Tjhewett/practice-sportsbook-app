import React, { useEffect, useState } from 'react';
import '../styles/betsforweek1.css'; 

const BetsforWeek1 = () => {
  const [week1Odds, setWeek1Odds] = useState([]);
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

    // Fetch the week 1 odds from the API
    const fetchWeek1Odds = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/week1_odds');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setWeek1Odds(data);
      } catch (error) {
        console.error('There was an error fetching the week 1 odds:', error);
      }
    };

    fetchUserCurrency();
    fetchWeek1Odds();
  }, []);

  const handleBetAmountChange = (gameId, amount) => {
    setBetAmounts(prev => ({ ...prev, [gameId]: amount }));
  };

  const submitBet = async (betType, gameId, amount, odds) => {
    // Ensure that the bet amount is a number and is positive
    amount = parseFloat(amount);
    if (isNaN(amount) || amount <= 0 || amount > userCurrency) {
      alert('Please enter a valid bet amount within your currency limits.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/place_bet_week1', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          game_id: gameId,
          bet_type: betType,
          odds: odds,
          amount: amount
        })
      });

      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      setUserCurrency(data.newCurrency); // Update user currency
      setBetAmounts(prev => ({ ...prev, [gameId]: '' }));
    } catch (error) {
      console.error('Error placing bet:', error);
      alert('There was an error placing your bet.');
    }
  };

  return (
    <div className="week1-odds-container">
      <h2>Week 1 Odds</h2>
      <div>Your Currency: ${userCurrency}</div>
      <div className="odds-table">
        {week1Odds.map(game => (
          <div key={game.id} className="odds-row">
            {/* Home team */}
            <div className="odds-team">{game.Home} (H)</div>
            <button onClick={() => submitBet('HomeSpread', game.id, betAmounts[game.id], game.Home_spread_odds)}>
               {game.Home_spread} {game.Home_spread_odds} 
            </button>
            <button onClick={() => submitBet('HomeML', game.id, betAmounts[game.id], game.Home_ml)}>
              {game.Home_ml} 
            </button>

            {/* Away team */}
            <div className="odds-team">{game.Away} (A)</div>
            <button onClick={() => submitBet('AwaySpread', game.id, betAmounts[game.id], game.Away_spread_odds)}>
              {game.Away_spread} {game.Away_spread_odds}
            </button>
            <button onClick={() => submitBet('AwayML', game.id, betAmounts[game.id], game.Away_ml)}>
              {game.Away_ml}
            </button>

            {/* Total points */}
            <div className="odds-team">Total:</div>
            <button onClick={() => submitBet('OverTotal', game.id, betAmounts[game.id], game.game_total_odds)}>
              O {game.game_total} {game.game_total_odds}
            </button>
            <button onClick={() => submitBet('UnderTotal', game.id, betAmounts[game.id], game.game_total_odds)}>
              U {game.game_total} {game.game_total_odds}
            </button>

            {/* Input for bet amount */}
            <input
              type="number"
              value={betAmounts[game.id] || ''}
              onChange={(e) => handleBetAmountChange(game.id, e.target.value)}
              min="1"
              max={userCurrency}
              placeholder="Bet amount"
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default BetsforWeek1;