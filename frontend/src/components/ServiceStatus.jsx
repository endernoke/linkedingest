import React from 'react';
import { useBackend } from '../context/BackendContext';

function ServiceStatus() {
  const { isBackendHealthy, error } = useBackend();

  if (isBackendHealthy === null) {
    return (
      <div className="max-w-2xl mx-auto mb-8 p-4 bg-gray-50 rounded-md border border-gray-200">
        <p className="text-gray-600">Checking service status...</p>
      </div>
    );
  }

  if (!isBackendHealthy) {
    return (
      <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-50 rounded-md border border-red-200 flex items-center">
        <div className="text-red-700 text-2xl mr-4">⚠️</div>
        <div>
          <p className="text-red-700">
            Service is temporarily unavailable. Please try again later.
          </p>
          { error && (
            <p className="text-red-700">
              {'Error: ' + error}
            </p>
          )}
        </div>
      </div>
    );
  }

  return null;
}

export default ServiceStatus;