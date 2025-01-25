import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function SearchForm() {
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (userId.trim()) {
      navigate(`/in/${userId.trim()}`);
      setUserId('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
      <label htmlFor="userId">LinkedIn User ID: </label>
      <input
        type="text"
        id="userId"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        placeholder="Enter LinkedIn ID"
        required
      />
      <button type="submit">Get Profile</button>
    </form>
  );
}

export default SearchForm;