import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SearchForm() {
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (userId.trim()) {
      navigate(`/in/${userId.trim()}`);
      setUserId('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8 max-w-2xl mx-auto">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-grow">
          <label htmlFor="userId" className="block text-sm font-medium text-gray-700 mb-2">
            LinkedIn User ID
          </label>
          <input
            type="text"
            id="userId"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter LinkedIn ID (e.g. john-doe-123)"
            className="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-linkedin-blue focus:border-linkedin-blue"
            required
          />
        </div>
        <button
          type="submit"
          className="inline-flex justify-center px-6 py-2 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-linkedin-blue hover:bg-linkedin-darker focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-linkedin-blue transition-colors sm:mt-6"
        >
          Get Profile
        </button>
      </div>
    </form>
  );
}

export default SearchForm;