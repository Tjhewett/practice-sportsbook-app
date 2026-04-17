import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import '../styles/account.css';

const AccountPage = () => {
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    created_at: '',
    currency: 0
  });
  const [bets, setBets] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('http://127.0.0.1:5000/api/account', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!res.ok) throw new Error('Failed to fetch account details');
        const data = await res.json();
        setUserData(data);

        const betsRes = await fetch('http://127.0.0.1:5000/api/user_bets', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (!betsRes.ok) throw new Error('Failed to fetch bets');
        const betsData = await betsRes.json();
        setBets(betsData);        
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="account-container">
      <h2>Account Information</h2>
      {error ? <p>{error}</p> : (
        <>
          <Table bordered size="sm">
            <tbody>
              <tr>
                <td className="label-column">Username</td>
                <td className="value-column">{userData.username}</td>
              </tr>
              <tr>
                <td className="label-column">Email</td>
                <td className="value-column">{userData.email}</td>
              </tr>
              <tr>
                <td className="label-column">Account Created</td>
                <td className="value-column">{userData.created_at}</td>
              </tr>
              <tr>
                <td className="label-column">Currency</td>
                <td className="value-column">${userData.currency.toFixed(2)}</td>
              </tr>
            </tbody>
          </Table>
          <h2>Betting History</h2>
          <Table bordered size="sm">
            <thead>
              <tr>
                <th>Bet Type</th>
                <th>Details</th>
                <th>Amount</th>
                <th>Odds</th>
                <th>Potential Payout</th>
                <th>Placed At</th>
                <th>Bet Evaluated?</th>
              </tr>
            </thead>
            <tbody>
              {bets.map((bet, index) => (
                <tr key={index}>
                  <td>{bet.bet_type || "SuperBowl"}</td>
                  <td>{bet.bet_type_details || bet.team || "Pick #" + bet.pick_number}</td>
                  <td>${bet.amount}</td>
                  <td>{bet.odds}</td>
                  <td>${bet.potential_payout.toFixed(2)}</td>
                  <td>{new Date(bet.placed_at).toLocaleString()}</td>
                  <td>{bet.is_evaluated.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}
    </div>
  );
};

export default AccountPage;