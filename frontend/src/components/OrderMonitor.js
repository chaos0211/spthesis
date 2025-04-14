// frontend/src/components/OrderMonitor.js
import { useState, useEffect } from 'react';
import axios from 'axios';

function OrderMonitor() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/order/list', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setOrders(response.data);
    } catch (error) {
      alert('Failed to fetch orders');
    }
  };

  return (
    <div>
      <h2>Order Monitor</h2>
      <ul>
        {orders.map((o) => (
          <li key={o.id}>
            Product: {o.product_name}, Quantity: {o.quantity}, Total: ${o.total_price}, Status: {o.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default OrderMonitor;