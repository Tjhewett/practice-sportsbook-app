import React, { useState, useEffect } from 'react';
import '../styles/playerstats.css'

const PlayerStats = () => {
  const [stats, setStats] = useState([]);
  const [currentStatCategory, setCurrentStatCategory] = useState('field_goals'); 
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(20); // Number of records per page
  const [totalPages, setTotalPages] = useState(0);

  const statCategories = ['field_goals', 'interceptions', 'passing', 'receiving', 'rushing', 'tackles'];

  const renderTableHeaders = () => {
    switch (currentStatCategory) {
      case 'field_goals':
        return (<><th>Player</th><th>FGM</th><th>Att</th><th>FG_percent</th><th>Lng</th><th>FG_Blk</th></>);
      case 'interceptions':
        return (<><th>Player</th><th>INT</th><th>INT_TD</th><th>INT_Yds</th><th>Lng</th></>);
      case 'passing':
        return (<><th>Player</th><th>Pass_Yds</th><th>Att</th><th>Cmp</th><th>TD</th><th>INT</th><th>Rate</th><th>Sck</th></>);
      case 'receiving':
        return (<><th>Player</th><th>Rec</th><th>Yds</th><th>TD</th><th>LNG</th><th>Rec_FUM</th><th>Tgts</th></>);
      case 'rushing':
        return (<><th>Player</th><th>Rush_Yds</th><th>Att</th><th>TD</th><th>Lng</th><th>Rush_FUM</th></>);
      case 'tackles':
        return (<><th>Player</th><th>Comb</th><th>Asst</th><th>Solo</th><th>Sck</th></>);
      default:
        return null;
    }
  };

  const renderTableRows = () => {
    switch (currentStatCategory) {
      case 'field_goals':
        return stats && stats.length > 0 ? stats.map((stat, index) => (
          <tr key={index}>
            <td>{stat.Player}</td>
            <td>{stat.FGM}</td>
            <td>{stat.Att}</td>
            <td>{stat.FG_percent}</td>
            <td>{stat.Lng}</td>
            <td>{stat.FG_Blk}</td>
          </tr>
        )) : <tr><td colSpan="the number of columns">No data available</td></tr>;
      case 'interceptions':
        return stats && stats.length > 0 ? stats.map((stat, index) => (
            <tr key={index}>
              <td>{stat.Player}</td>
              <td>{stat.INT}</td>
              <td>{stat.INT_TD}</td>
              <td>{stat.INT_Yds}</td>
              <td>{stat.Lng}</td>
            </tr>
        )) : <tr><td colSpan="the number of columns">No data available</td></tr>;
      case 'passing':
        return stats && stats.length > 0 ? stats.map((stat, index) => (
          <tr key={index}>
            <td>{stat.Player}</td>
            <td>{stat.Pass_Yds}</td>
            <td>{stat.Att}</td>
            <td>{stat.Cmp}</td>
            <td>{stat.TD}</td>
            <td>{stat.INT}</td>
            <td>{stat.Rate}</td>
            <td>{stat.Sck}</td>
          </tr>
        )) : <tr><td colSpan="the number of columns">No data available</td></tr>;
      case 'receiving':
        return stats && stats.length > 0 ? stats.map((stat, index) => (
          <tr key={index}>
            <td>{stat.Player}</td>
            <td>{stat.Rec}</td>
            <td>{stat.Yds}</td>
            <td>{stat.TD}</td>
            <td>{stat.LNG}</td>
            <td>{stat.Rec_FUM}</td>
            <td>{stat.Tgts}</td>
          </tr>
        )) : <tr><td colSpan="the number of columns">No data available</td></tr>;
      case 'rushing':
        return stats && stats.length > 0 ? stats.map((stat, index) => (
            <tr key={index}>
              <td>{stat.Player}</td>
              <td>{stat.Rush_Yds}</td>
              <td>{stat.Att}</td>
              <td>{stat.TD}</td>
              <td>{stat.Lng}</td>
              <td>{stat.Rush_FUM}</td>
            </tr>
        )) : <tr><td colSpan="the number of columns">No data available</td></tr>;
      case 'tackles':
        return stats && stats.length > 0 ? stats.map((stat, index) => (
            <tr key={index}>
              <td>{stat.Player}</td>
              <td>{stat.Comb}</td>
              <td>{stat.Asst}</td>
              <td>{stat.Solo}</td>
              <td>{stat.Sck}</td>
            </tr>
        )) : <tr><td colSpan="the number of columns">No data available</td></tr>;
      default:
        return null;
    }
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };
  
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/${currentStatCategory}?page=${currentPage}&size=${pageSize}`);
        const data = await response.json();
        setStats(data.items); 
        setTotalPages(data.pages);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
    fetchStats();
  }, [currentStatCategory, currentPage, pageSize]);

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

    <div className="pagination">
      <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
        Previous
      </button>
      <span>Page {currentPage} of {totalPages}</span>
      <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
        Next
      </button>
    </div>

    </div>
  );
};

export default PlayerStats;

