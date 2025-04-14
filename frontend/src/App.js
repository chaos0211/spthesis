// frontend/src/App.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import ProductManage from './components/ProductManage';
import OrderMonitor from './components/OrderMonitor';
import Analytics from './components/Analytics';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/seller/products" element={<ProductManage />} />
        <Route path="/seller/orders" element={<OrderMonitor />} />
        <Route path="/seller/analytics" element={<Analytics />} />
      </Routes>
    </Router>
  );
}

export default App;