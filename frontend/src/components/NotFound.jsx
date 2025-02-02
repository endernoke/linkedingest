import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function NotFound({ requestedUserId = '' }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [isConnecting, setIsConnecting] = useState(false);

  const handleConnect = () => {
    setIsConnecting(true);
    setTimeout(() => {
      window.location.reload();
    }, 1000);
  };

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            404 - A Missed Connection
          </h1>
          <p className="text-gray-600">
            This page is out for a coffee chat. Please double check the user ID and try again.
          </p>
        </div>

        {/* Mock Profile Card */}
        <div className="border rounded-lg p-6 mb-8">
          <div className="flex items-center space-x-4">
            <div className="w-24 h-24 bg-gradient-to-br from-gray-200 to-gray-300 rounded-full flex items-center justify-center">
              <span className="text-4xl">👻</span>
            </div>
            <div>
              <h2 className="text-xl font-semibold">
                {requestedUserId || 'LinkedIn Member'}
              </h2>
              <p className="text-gray-600">
                21x Hide-and-Seek Wins
              </p>
              <p className="text-sm text-gray-500">
                Location not found
              </p>
            </div>
          </div>

          <div className="mt-4 border-t pt-4">
            <p className="text-gray-700">
              I specialize in disappearing from URLs and making developers question their routing logic. <br />
              If you believe I rejected your connection request by mistake, you could try again. Hopefully you won't get another 404.
            </p>
          </div>

          <div className="mt-4">
            <div className="text-sm text-gray-600 mb-2">Skills</div>
            <div className="flex flex-wrap gap-2">
              {['Ninja Skills', 'Error Generation', 'Route Confusion', 'Making Developers Cry'].map(skill => (
                <span key={skill} className="bg-gray-100 px-3 py-1 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={handleConnect}
            disabled={isConnecting}
            className={`inline-flex justify-center items-center px-6 py-2 border border-linkedin-blue 
              rounded-full shadow-sm text-base font-medium 
              ${isConnecting? 'text-linkedin-blue bg-white' : 'text-white bg-linkedin-blue'}
              ${isConnecting? 'hover:bg-gray-200 hover:text-linkedin-darker hover:border-linkedin-darker' : 'hover:bg-linkedin-darker'}
              focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-linkedin-blue 
              transition-colors`}
            >
            {isConnecting ? (
              <>
                <svg className="-ml-1 mr-3 h-5 w-5 text-linkedin-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Pending
              </>
            ) : (
              <>
                <svg className="-ml-1 mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8 9a3 3 0 100-6 3 3 0 000 6zm-4 8a4 4 0 018 0H4zm9-8a1 1 0 112 0v2h2a1 1 0 110 2h-2v2a1 1 0 11-2 0v-2h-2a1 1 0 110-2h2V9z" />
                </svg>
                Connect
              </>
            )}
          </button>
          <button
            onClick={() => navigate('/')}
            className="inline-flex justify-center px-6 py-2 border border-gray-300 
              rounded-full shadow-sm text-base font-medium text-gray-700 bg-white 
              hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 
              focus:ring-linkedin-blue transition-colors"
            >
            Back to Homepage
          </button>
        </div>
      </div>
    </div>
  );
}

export default NotFound;