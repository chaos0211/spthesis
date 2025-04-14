// frontend/src/components/ProductManage.js
import { useState, useEffect } from 'react';
import axios from 'axios';

function ProductManage() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: '', description: '', price: '', stock: '' });

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/product/list', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setProducts(response.data);
    } catch (error) {
      alert('Failed to fetch products');
    }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/product/add', form, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      fetchProducts();
      setForm({ name: '', description: '', price: '', stock: '' });
    } catch (error) {
      alert('Failed to add product');
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/api/product/delete/${id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      fetchProducts();
    } catch (error) {
      alert('Failed to delete product');
    }
  };

  return (
    <div>
      <h2>Manage Products</h2>
      <form onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <input
          type="number"
          placeholder="Price"
          value={form.price}
          onChange={(e) => setForm({ ...form, price: e.target.value })}
        />
        <input
          type="number"
          placeholder="Stock"
          value={form.stock}
          onChange={(e) => setForm({ ...form, stock: e. value })}
        />
        <button type="submit">Add Product</button>
      </form>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            {p.name} - ${p.price} - Stock: {p.stock}
            <button onClick={() => handleDelete(p.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductManage;