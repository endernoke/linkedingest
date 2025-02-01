import React from 'react';
import config from '../config';

function Footer() {
  return (
    <footer className="bg-white border-t mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex gap-4">
            <a 
              href={config.app.github.issues.feature}
              target="_blank"
              rel="noopener noreferrer"
              className={`text-${config.theme.colors.text} hover:text-${config.theme.colors.primary} transition-colors`}
            >
              Request a feature
            </a>
            <span className="text-gray-300">|</span>
            <a 
              href={config.app.github.issues.bug}
              target="_blank"
              rel="noopener noreferrer"
              className={`text-${config.theme.colors.text} hover:text-${config.theme.colors.primary} transition-colors`}
            >
              Report a bug
            </a>
          </div>
          <div className={`text-${config.theme.colors.text}`}>
            Made with <span role="img" aria-label="saluting face">🫡</span> by{' '}
            <a 
              href={config.author.profile}
              target="_blank"
              rel="noopener noreferrer"
              className={`text-${config.theme.colors.primary} hover:text-${config.theme.colors.primaryDark} transition-colors`}
            >
              {config.author.name}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;