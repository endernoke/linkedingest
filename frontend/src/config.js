export const config = {
  app: {
    name: (import.meta.env.VITE_APP_NAME) || "LinkedIngest",
    description: (import.meta.env.VITE_APP_DESCRIPTION) || "Turn LinkedIn profiles into AI-friendly text ingests",
    baseUrl: "linkedingest.onrender.com",
    github: {
      repo: 'https://github.com/endernoke/linkedingest',
      issues: {
        feature: 'https://github.com/endernoke/linkedingest/issues/new?template=feature_request.md',
        bug: 'https://github.com/endernoke/linkedingest/issues/new?template=bug_report.md'
      }
    }
  },
  author: {
    name: '@endernoke',
    profile: 'https://www.linkedin.com/in/james-zheng-zi'
  },
  theme: {
    colors: {
      primary: 'linkedin-blue',
      primaryLight: 'linkedin-lighter',
      primaryDark: 'linkedin-darker',
      text: 'gray-600',
      textDark: 'gray-900'
    }
  },
  api: {
    baseUrl: '/api',
    endpoints: {
      health: '/health',
      queue: '/queue',
      profile: '/profile'
    }
  },
  exampleProfiles: ["jeffweiner08", "gretchenrubin", "neil123", "melindagates", "john-smith-5065b4349"],
  is_demo: true
};

export default config;