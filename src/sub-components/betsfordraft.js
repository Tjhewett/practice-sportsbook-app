import React, { useEffect, useState, useMemo } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/betsfordraft.css'

const BetsforDraft = () => {
  const [userCurrency, setUserCurrency] = useState(0);
  const [betAmounts, setBetAmounts] = useState({});
  const [oddsData, setOddsData] = useState({});

  const picks = useMemo(() => [1, 2, 3, 4, 5], []);

  // Function to fetch odds for a specific pick
  const fetchDraftOdds = async (pickNumber) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/draft_odds_pick${pickNumber}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch odds for pick ${pickNumber}`);
      }
      const data = await response.json();
      setOddsData(prev => ({ ...prev, [pickNumber]: data }));
    } catch (error) {
      console.error(`There has been a problem fetching odds for pick ${pickNumber}:`, error);
    }
  };

  useEffect(() => {
    picks.forEach(pickNumber => fetchDraftOdds(pickNumber)); // Fetch odds for each pick

    // Fetch user's currency
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
  
    fetchUserCurrency();
  }, [picks]);

  // Handle bet amount changes
  const handleBetAmountChange = (player, pickNumber, amount) => {
    setBetAmounts(prev => ({ ...prev, [`${pickNumber}-${player}`]: amount }));
  };

  // Handle placing a bet
  const handlePlaceBet = async (player, pickNumber, id, odds) => {
    const amount = betAmounts[`${pickNumber}-${player}`] || 0;
    if (amount <= 0 || amount > userCurrency) {
      alert('Invalid bet amount');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/place_bet_draft', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ id, pick_number: pickNumber, amount, odds })
      });

      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      setUserCurrency(data.newCurrency); // Update user currency
      setBetAmounts(prev => ({ ...prev, [`${pickNumber}-${player}`]: '' })); // Reset the bet amount
    } catch (error) {
      console.error('Error placing bet:', error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="currency">Your Currency: ${userCurrency}</div>
      {picks.map(pickNumber => (
        <div key={pickNumber}>
          <h2>Draft Odds - Pick {pickNumber}</h2>
          <table className="table1">
            <tbody>
              {oddsData[pickNumber]?.map((odd) => (
                <tr key={odd.Player}>
                  <td>{odd.Player}</td>
                  <td>
                    <input
                      type="number"
                      value={betAmounts[`${pickNumber}-${odd.Player}`] || ''}
                      onChange={(e) => handleBetAmountChange(odd.Player, pickNumber, e.target.value)}
                      min="1"
                      max={userCurrency}
                      placeholder="Bet amount"
                    />
                    <button className="btn-primary" onClick={() => handlePlaceBet(odd.Player, pickNumber, odd.id, odd.Odds)}>
                      {odd.Odds}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};

export default BetsforDraft;
