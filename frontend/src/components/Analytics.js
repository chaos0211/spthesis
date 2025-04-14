// frontend/src/components/Analytics.js
import { useState, useEffect } from 'react';
import axios from 'axios';

function Analytics() {
  const [report, setReport] = useState([]);

  useEffect(() => {
    fetchReport();
  }, []);

  const fetchReport = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/analytics/sales', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setReport(response.data);
    } catch (error) {
      alert('Failed to fetch report');
    }
  };

  return (
    <div>
      <h2>Sales Report</h2>
      <ul>
        {report.map((r, index) => (
          <li key={index}>
            Product: {r.product}, Total Sales: ${r.total_sales}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Analytics;