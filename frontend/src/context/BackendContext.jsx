import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const BackendContext = createContext();

export function BackendProvider({ children }) {
  const [isBackendHealthy, setIsBackendHealthy] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        await axios.get('/api/health');
        setIsBackendHealthy(true);
        setError(null);
      } catch (err) {
        setIsBackendHealthy(false);
        setError(err.response?.data?.detail || 'Service temporarily unavailable');
      }
    };

    checkBackendHealth();
  }, []);

  return (
    <BackendContext.Provider value={{ isBackendHealthy, error }}>
      {children}
    </BackendContext.Provider>
  );
}

export function useBackend() {
  return useContext(BackendContext);
}