import React from 'react';

function ProfileDisplay({ profile }) {
  const formattedData = JSON.stringify(profile, null, 2);

  return (
    <div className="profile-container max-w-4xl mx-auto">
      <div className="bg-white shadow-sm rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Profile Data</h2>
        <textarea
          value={formattedData}
          readOnly
          className="w-full h-[600px] font-mono text-sm bg-gray-50 p-4 rounded-md border border-gray-200 focus:border-linkedin-blue focus:ring-linkedin-blue"
        />
      </div>
    </div>
  );
}

export default ProfileDisplay;