import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBackend } from '../context/BackendContext';
import { isValidLinkedInId } from '../utils/validation';

function SearchForm() {
  const [userId, setUserId] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { isBackendHealthy } = useBackend();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedId = userId.trim();
    
    if (!isValidLinkedInId(trimmedId)) {
      setError('Invalid LinkedIn ID format. Please check your input.');
      return;
    }

    navigate(`/in/${trimmedId}`);
    setError('');
  };

  const handleInputChange = (e) => {
    setUserId(e.target.value);
    setError(''); // Clear error when user types
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8 max-w-2xl mx-auto relative">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-grow relative">
          <label htmlFor="userId" className="block text-sm font-medium text-gray-700 mb-2">
            LinkedIn User ID
          </label>
          <input
            type="text"
            id="userId"
            value={userId}
            onChange={handleInputChange}
            placeholder="Enter LinkedIn ID (e.g. john-doe-123)"
            className={`w-full px-4 py-2 border rounded-md shadow-sm 
              ${error ? 'border-red-500 focus:ring-red-500 focus:border-red-500' 
                     : 'border-gray-300 focus:ring-linkedin-blue focus:border-linkedin-blue'}`}
            required
            disabled={!isBackendHealthy}
          />
        </div>
        <div className="sm:self-end">
          <button
            type="submit"
            className="inline-flex justify-center px-6 py-2 border border-transparent shadow-sm 
              text-base font-medium rounded-md text-white bg-linkedin-blue 
              hover:bg-linkedin-darker focus:outline-none focus:ring-2 
              focus:ring-offset-2 focus:ring-linkedin-blue transition-colors duration-200 sm:mt-6
              disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!isBackendHealthy}
          >
            Get Profile
          </button>
        </div>
      </div>
      {error && (
        <p className="absolute top-[72px] left-0 text-sm text-red-600">
          {error}
        </p>
      )}
    </form>
  );
}

export default SearchForm;