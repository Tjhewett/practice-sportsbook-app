import React, { useState, useEffect } from 'react';
import '../styles/teamstats.css'

const TeamStats = () => {
  const [stats, setStats] = useState([]);
  const [currentStatCategory, setCurrentStatCategory] = useState('team_passing'); 


  const statCategories = ['team_passing', 'team_rushing', 'team_receiving', 'team_defense_passing', 'team_defense_rushing', 'team_defense_receiving'];

  const renderTableHeaders = () => {
    switch (currentStatCategory) {
      case 'team_passing':
        return (<><th>Team</th><th>Att</th><th>Cmp</th><th>Cmp_percent</th><th>Pass_Yds</th><th>TD</th><th>INT</th><th>Rate</th><th>Sck</th><th>SckY</th></>);
      case 'team_rushing':
        return (<><th>Team</th><th>Att</th><th>Rush_Yds</th><th>YPC</th><th>TD</th><th>Rush_FUM</th></>);
      case 'team_receiving':
        return (<><th>Team</th><th>Rec</th><th>Yds</th><th>TD</th><th>Rec_FUM</th></>);
      case 'team_defense_passing':
        return (<><th>Team</th><th>Att</th><th>Cmp</th><th>Cmp_percent</th><th>Yds</th><th>TD</th><th>INT</th><th>Rate</th><th>Sck</th></>);
      case 'team_defense_rushing':
        return (<><th>Team</th><th>Att</th><th>Rush_Yds</th><th>YPC</th><th>TD</th><th>Rush_FUM</th></>);
      case 'team_defense_receiving':
        return (<><th>Team</th><th>Rec</th><th>Yds</th><th>TD</th><th>Rec_FUM</th><th>PDef</th></>);
      default:
        return null;
    }
  };

  const renderTableRows = () => {
    switch (currentStatCategory) {
      case 'team_passing':
        return stats.map((stat, index) => (
          <tr key={index}>
            <td>{stat.Team}</td>
            <td>{stat.Att}</td>
            <td>{stat.Cmp}</td>
            <td>{stat.Cmp_percent}</td>
            <td>{stat.Pass_Yds}</td>
            <td>{stat.TD}</td>
            <td>{stat.INT}</td>
            <td>{stat.Rate}</td>
            <td>{stat.Sck}</td>
            <td>{stat.SckY}</td>
          </tr>
        ));
      case 'team_rushing':
        return stats.map((stat, index) => (
            <tr key={index}>
              <td>{stat.Team}</td>
              <td>{stat.Att}</td>
              <td>{stat.Rush_Yds}</td>
              <td>{stat.YPC}</td>
              <td>{stat.TD}</td>
              <td>{stat.Rush_FUM}</td>
            </tr>
        ));
      case 'team_receiving':
        return stats.map((stat, index) => (
          <tr key={index}>
            <td>{stat.Team}</td>
            <td>{stat.Rec}</td>
            <td>{stat.Yds}</td>
            <td>{stat.TD}</td>
            <td>{stat.Rec_FUM}</td>
          </tr>
        ));
      case 'team_defense_passing':
        return stats.map((stat, index) => (
          <tr key={index}>
            <td>{stat.Team}</td>
            <td>{stat.Att}</td>
            <td>{stat.Cmp}</td>
            <td>{stat.Cmp_percent}</td>
            <td>{stat.Yds}</td>
            <td>{stat.TD}</td>
            <td>{stat.INT}</td>
            <td>{stat.Rate}</td>
            <td>{stat.Sck}</td>
          </tr>
        ));
      case 'team_defense_rushing':
        return stats.map((stat, index) => (
            <tr key={index}>
              <td>{stat.Team}</td>
              <td>{stat.Att}</td>
              <td>{stat.Rush_Yds}</td>
              <td>{stat.YPC}</td>
              <td>{stat.TD}</td>
              <td>{stat.Rush_FUM}</td>
            </tr>
        ));
      case 'team_defense_receiving':
        return stats.map((stat, index) => (
            <tr key={index}>
              <td>{stat.Team}</td>
              <td>{stat.Rec}</td>
              <td>{stat.Yds}</td>
              <td>{stat.TD}</td>
              <td>{stat.Rec_FUM}</td>
              <td>{stat.PDef}</td>
            </tr>
        ));
      default:
        return null;
    }
  };

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/${currentStatCategory}`);
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchStats();
  }, [currentStatCategory]);

  return (
    <div>
      <nav>
        {statCategories.map(category => (
          <button key={category} onClick={() => setCurrentStatCategory(category)}>
            {category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')}
          </button>
        ))}
      </nav>

      <h2>{currentStatCategory.charAt(0).toUpperCase() + currentStatCategory.slice(1).replace('_', ' ')} Stats</h2>    

      <table>
        <thead>
          <tr>{renderTableHeaders()}</tr>
        </thead>
        <tbody>
          {renderTableRows()}
        </tbody>
      </table>
    </div>
  );
};

export default TeamStats;

