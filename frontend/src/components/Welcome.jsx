import React from 'react';
import { useNavigate } from 'react-router-dom';
import config from '../config';

function Welcome() {
  const navigate = useNavigate();

  const handleExampleClick = (profileId) => {
    navigate(`/in/${profileId}`);
  };

  return (
    <div className="max-w-4xl mx-auto mb-12">
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h2 className={`text-2xl font-semibold text-${config.theme.colors.primary} mb-6`}>
          {config.app.description}
        </h2>
        
        <div className="space-y-6">
          <div>
            <h3 className={`text-lg font-medium text-${config.theme.colors.textDark} mb-2`}>
              How It Works
            </h3>
            <p className={`text-${config.theme.colors.text}`}>
              Simply enter a LinkedIn profile ID or append it to the URL to generate a structured text ingest that's optimized for feeding to large language models.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-4 border border-gray-100 rounded-md">
              <div className={`text-${config.theme.colors.primary} mb-2`}>1. Enter Profile ID</div>
              <p className={`text-sm text-${config.theme.colors.text}`}>
                Use the search bar to input a LinkedIn profile ID (e.g., john-doe-123)
              </p>
            </div>
            <div className="p-4 border border-gray-100 rounded-md">
              <div className={`text-${config.theme.colors.primary} mb-2`}>2. Generate Ingest</div>
              <p className={`text-sm text-${config.theme.colors.text}`}>
                The profile will be transformed into a structured text ingest
              </p>
            </div>
            <div className="p-4 border border-gray-100 rounded-md">
              <div className={`text-${config.theme.colors.primary} mb-2`}>3. Feed to LLMs</div>
              <p className={`text-sm text-${config.theme.colors.text}`}>
                Copy the generated text to use with any large language model (LLM)
              </p>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-md">
            <h3 className={`text-lg font-medium text-${config.theme.colors.textDark} mb-2`}>
              Quick Tip
            </h3>
            <p className={`text-sm text-${config.theme.colors.text}`}>
              You can directly access any profile by replacing 
              <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                linkedin.com
              </code>
               with 
              <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                {config.app.baseUrl}
              </code>
                in the URL of the profile you want to ingest. For example, <br />
              <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                {config.app.baseUrl+'/in/john-doe-123'}
              </code>
            </p>
          </div>

          <div className="border-t pt-6">
            <h3 className={`text-lg font-medium text-${config.theme.colors.textDark} mb-4`}>
              Try these example profiles:
            </h3>
            <div className="flex flex-wrap gap-2">
              {config.exampleProfiles.map(profileId => (
                <button
                  key={profileId}
                  onClick={() => handleExampleClick(profileId)}
                  className="px-4 py-2 rounded-full border border-linkedin-blue text-linkedin-blue 
                    hover:bg-linkedin-blue hover:text-white transition-colors duration-200"
                >
                  {profileId}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Welcome;