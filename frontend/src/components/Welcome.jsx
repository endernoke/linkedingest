import React from 'react';

function Welcome() {
  return (
    <div className="max-w-4xl mx-auto mb-12">
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h2 className="text-2xl font-semibold text-linkedin-blue mb-6">
          Transform LinkedIn Profiles into Prompt-Ready Data
        </h2>
        
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              How It Works
            </h3>
            <p className="text-gray-600">
              Simply enter a LinkedIn profile ID or append it to the URL to generate a structured text ingest that's optimized for feeding to large language models.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-4 border border-gray-100 rounded-md">
              <div className="text-linkedin-blue mb-2">1. Enter Profile ID</div>
              <p className="text-sm text-gray-600">
                Use the search bar to input a LinkedIn profile ID (e.g., john-doe-123)
              </p>
            </div>
            <div className="p-4 border border-gray-100 rounded-md">
              <div className="text-linkedin-blue mb-2">2. Generate Ingest</div>
              <p className="text-sm text-gray-600">
                The profile will be transformed into a structured text ingest
              </p>
            </div>
            <div className="p-4 border border-gray-100 rounded-md">
              <div className="text-linkedin-blue mb-2">3. Feed to LLMs</div>
              <p className="text-sm text-gray-600">
                Copy the generated text to use with any large language model (LLM)
              </p>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-md">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Quick Tip
            </h3>
            <p className="text-sm text-gray-600">
              You can directly access any profile by replacing 
              <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                linkedin.com
              </code>
               with 
              <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                linkedingest.vercel.app
              </code>
                in the URL of the profile you want to ingest. For example, <br />
              <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                linkedingest.vercel.app/in/john-doe-123
              </code>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Welcome;