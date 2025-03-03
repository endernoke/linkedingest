import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import useCountdown from '../hooks/useCountdown';
import axios from 'axios';
import ProfileDisplay from './ProfileDisplay';
import NotFound from './NotFound';
import config from '../config';

function ProfilePage() {
  const location = useLocation();
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [serverQueueStatus, setServerQueueStatus] = useState(null);
  const timeLeft = useCountdown(serverQueueStatus?.estimated_completion_timestamp);

  // Extract clean profile ID from path
  const profileId = location.pathname
    .split('/in/')[1]  // Get everything after /in/
    .split('/')[0];    // Get first segment before any trailing slash

  useEffect(() => {
    const getServerQueueStatus = async () => {
      try {
        const response = await axios.get(`${config.api.baseUrl+config.api.endpoints.queue}`);
        console.log(response)
        setServerQueueStatus(response.data);
      } catch (error) {
        console.error('Failed to fetch server queue status:', error);
        setServerQueueStatus({ error: error });
      }
    };

    const fetchProfile = async () => {
      try {
        setError(null);
        setProfileData(null);
        setLoading(true);
        const response = await axios.get(`${config.api.baseUrl+config.api.endpoints.profile}/${profileId}`);
        setProfileData(response.data);
      } catch (error) {
        setError({
          status: error?.response?.status || (error.request ? 444 : 'Unknown'),
          detail: error?.response?.data?.detail || error?.message
        });
        setProfileData(null);
      } finally {
        setLoading(false);
        setServerQueueStatus(null);
      }
    };

    if (profileId) {
      getServerQueueStatus();
      fetchProfile();
    }

    // Cleanup function
    return () => {
      setError(null);
      setProfileData(null);
      setLoading(false);
      setServerQueueStatus(null);
    };
  }, [profileId]);
  
  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-linkedin-blue mb-4"></div>
        <p className="text-gray-700">Loading profile of {profileId}...</p>
        <p></p> {/* New line */}
        {serverQueueStatus?.waiting_requests_count ? (
          <p className="text-gray-700">
            Your request was in queue position {serverQueueStatus.waiting_requests_count}.
          </p>
        ) : null}
        {serverQueueStatus?.estimated_completion_timestamp && (
          <>
          {timeLeft && (
            <p className="text-gray-700">
              Estimated waiting time: {timeLeft.minutes}m {timeLeft.seconds}s
            </p>
          )}
          {/* We overestimated the waiting time, so show a generic message */}
          {! timeLeft && (
            <p className="text-gray-700">
              Estimated waiting time: less than 1 minute
            </p>
          )}
          </>
        )}
        {config.is_demo && (
          <div className="mt-12 p-8 bg-yellow-50 border border-yellow-900 rounded-lg max-w-2xl">
            <p className="text-yellow-700 font-bold text-lg text-center mb-2">
              This is a demo website with slower loading speed
            </p>
            <p className="text-yellow-700 text-left">
              I intentionally added a small delay in between API calls to LinkedIn in the backend in order to prevent my account from getting rate-limited and banned. This means loading profiles will take longer than usual.<br />
              For faster performance, consider hosting the application locally.
              <br /><br />
              {' '}
              <a 
                href={`${config.app.github.repo}/blob/main/LOCALHOST.md`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-linkedin-blue underline hover:text-linkedin-darker"
              >
                Learn more about hosting locally
              </a>
            </p>
          </div>
        )}
      </div>
    );
  }

  if (error) {
    if (error.status === 400) {
      return <NotFound requestedUserId={profileId} />;
    }

    return (
      <div className="max-w-2xl mx-auto mt-8">
        <div className="bg-red-50 rounded-lg p-6 border border-red-200">
          <div className="flex items-center">
            <div className="text-red-700 text-2xl mr-4">⚠️</div>
            <div className="flex-1">
              <h3 className="text-lg font-medium text-red-800 mb-2">
                {error.status === 500 && 'Internal Server Error'}
                {error.status === 444 && 'Connection Error'}
                {error.status !== 500 && error.status !== 444 && 'Unexpected Error'}
              </h3>
              <p className="text-red-700 mb-4">
                {error.status === 500 && 'Something went wrong on our end.'}
                {error.status === 444 && 'Could not connect to the server. Please check your connection.'}
                {error.status !== 500 && error.status !== 444 && 'An unexpected error occurred.'}
                {error.detail && (
                  <>
                    <br />
                    {`Details: ${error.detail}`}
                  </>
                )}
              </p>
              <div className="flex gap-4">
                <button
                  onClick={() => window.location.reload()}
                  className="inline-flex items-center px-4 py-2 border border-red-300 
                    rounded-md shadow-sm text-sm font-medium text-red-700 bg-white 
                    hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 
                    focus:ring-red-500 transition-colors"
                >
                  Try Again
                </button>
                <a
                  href={config.app.github.issues.bug}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-4 py-2 border border-transparent 
                    rounded-md shadow-sm text-sm font-medium text-white bg-red-600 
                    hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 
                    focus:ring-red-500 transition-colors"
                >
                  Report This Issue
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return profileData ? <ProfileDisplay profile={profileData} /> : null;
}

export default ProfilePage;