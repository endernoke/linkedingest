import React from 'react';

function ProfileDisplay({ profile }) {
  return (
    <div className="profile-container max-w-4xl mx-auto">
      <div className="bg-white shadow-sm rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Profile Ingest of {profile.full_name}
        </h2>
        <textarea
          value={
            profile.summary+
            (profile?.experience ? ("\n\n---\n\n"+profile.experience) : "")+
            (profile?.education ? ("\n\n---\n\n"+profile.education) : "")+
            (profile?.honors ? ("\n\n---\n\n"+profile.honors) : "")+
            (profile?.certifications ? ("\n\n---\n\n"+profile.certifications) : "")+
            (profile?.projects ? ("\n\n---\n\n"+profile.projects) : "")+
            (profile?.volunteer ? ("\n\n---\n\n"+profile.volunteer) : "")+
            (profile?.publications ? ("\n\n---\n\n"+profile.publications) : "")+
            (profile?.skills ? ("\n\n---\n\n"+profile.skills) : "")+
            (profile?.languages ? ("\n\n---\n\n"+profile.languages) : "")
          }
          className="w-full h-[600px] font-mono text-sm bg-gray-50 p-4 rounded-md border border-gray-200 focus:border-linkedin-blue focus:ring-linkedin-blue"
        />
      </div>
    </div>
  );
}

export default ProfileDisplay;