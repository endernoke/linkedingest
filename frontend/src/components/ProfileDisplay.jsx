import React from 'react';

function ProfileDisplay({ profile }) {
  const formattedData = JSON.stringify(profile, null, 2);

  return (
    <div className="profile-container">
      <textarea
        value={formattedData}
        className="profile-data"
        rows={20}
        style={{
          width: '100%',
          maxWidth: '600px',
          fontFamily: 'monospace',
          padding: '1rem',
          marginTop: '1rem'
        }}
      />
    </div>
  );
}

export default ProfileDisplay;