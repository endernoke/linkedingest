import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import ProfileDisplay from './ProfileDisplay';

function ProfilePage() {
  const { userId } = useParams();
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get(`/api/profile/${userId}`);
        setProfileData(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
        setError('Failed to load profile');
      }
    };

    if (userId) {
      fetchProfile();
    }
  }, [userId]);

  if (error) return <div>{error}</div>;
  if (!profileData) return <div>Loading...</div>;

  return <ProfileDisplay profile={profileData} />;
}

export default ProfilePage;