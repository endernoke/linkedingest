import React from 'react';

function Footer() {
  return (
    <footer className="bg-white border-t mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex gap-4">
            <a 
              href="https://github.com/endernoke/linkedingest/issues/new?template=feature_request.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-linkedin-blue transition-colors"
            >
              Request a feature
            </a>
            <span className="text-gray-300">|</span>
            <a 
              href="https://github.com/endernoke/linkedingest/issues/new?template=bug_report.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-linkedin-blue transition-colors"
            >
              Report a bug
            </a>
          </div>
          <div className="text-gray-600">
            Made with <span role="img" aria-label="saluting face">🫡</span> by{' '}
            <a 
              href="https://www.linkedin.com/in/james-zheng-zi"
              target="_blank"
              rel="noopener noreferrer"
              className="text-linkedin-blue hover:text-linkedin-darker transition-colors"
            >
              @endernoke
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;