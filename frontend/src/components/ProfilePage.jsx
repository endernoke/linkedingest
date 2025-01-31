import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import ProfileDisplay from './ProfileDisplay';
import NotFound from './NotFound';

function ProfilePage() {
  const location = useLocation();
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  // Extract clean profile ID from path
  const profileId = location.pathname
    .split('/in/')[1]  // Get everything after /in/
    .split('/')[0];    // Get first segment before any trailing slash

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setError(null);
        setProfileData(null);
        setLoading(true);
        const response = await axios.get(`/api/profile/${profileId}`);
        setProfileData(response.data);
      } catch (error) {
        setError('Failed to load profile. Please check the ID and try again.');
        setProfileData(null);
      } finally {
        setLoading(false);
      }
    };

    if (profileId) {
      fetchProfile();
    }

    // Cleanup function
    return () => {
      setError(null);
      setProfileData(null);
      setLoading(false);
    };
  }, [profileId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-linkedin-blue"></div>
      </div>
    );
  }

  if (error) {
    return <NotFound requestedUserId={profileId} />;
  }

  return profileData ? <ProfileDisplay profile={profileData} /> : null;
}

export default ProfilePage;