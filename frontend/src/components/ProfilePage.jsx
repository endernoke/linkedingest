import React, { useEffect, useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import axios from 'axios';
import ProfileDisplay from './ProfileDisplay';

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
        setLoading(true);
        const response = await axios.get(`/api/profile/${profileId}`);
        setProfileData(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
        setError('Failed to load profile. Please check the ID and try again.');
      } finally {
        setLoading(false);
      }
    };

    if (profileId) {
      fetchProfile();
    }
  }, [profileId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-linkedin-blue"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto mt-8 p-4 bg-red-50 rounded-md border border-red-200">
        <p className="text-red-700">{error}</p>
      </div>
    );
  }

  return <ProfileDisplay profile={profileData} />;
}

export default ProfilePage;