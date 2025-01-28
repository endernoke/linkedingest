import React, { useRef, useState, useEffect } from 'react';

function RibbonBar({ profile, visibleSections, setVisibleSections, onCopyAll, onDownload, onSectionCopy, onSectionScroll }) {
  const scrollContainerRef = useRef(null);
  const [showLeftScroll, setShowLeftScroll] = useState(false);
  const [showRightScroll, setShowRightScroll] = useState(false);

  // Check if scroll buttons should be shown
  const checkScroll = () => {
    const container = scrollContainerRef.current;
    if (container) {
      setShowLeftScroll(container.scrollLeft > 0);
      setShowRightScroll(
        container.scrollLeft < container.scrollWidth - container.clientWidth
      );
    }
  };

  // Add scroll event listener
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (container) {
      container.addEventListener('scroll', checkScroll);
      // Initial check
      checkScroll();
      return () => container.removeEventListener('scroll', checkScroll);
    }
  }, []);

  // Scroll handlers
  const scroll = (direction) => {
    const container = scrollContainerRef.current;
    if (container) {
      container.scrollBy({
        left: direction * 200,
        behavior: 'smooth'
      });
    }
  };

  return (
    <div className="sticky top-0 bg-white shadow-sm z-10 p-4 border-b">
      <div className="flex justify-between items-start mb-4">
        <h2 className="text-xl font-semibold text-gray-900 flex-1 mr-4">
          Profile Ingest of {profile.full_name}
        </h2>
        <div className="flex flex-col sm:flex-row gap-2">
          <button
            onClick={onCopyAll}
            className="inline-flex justify-center px-6 py-2 border border-transparent shadow-sm 
              text-base font-medium rounded-md text-linkedin-blue bg-white 
              hover:bg-gray-200 focus:outline-none focus:ring-2 
              focus:ring-offset-2 focus:ring-linkedin-blue transition-colors sm:mt-6"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
            </svg>
            Copy All
          </button>
          <button
            onClick={onDownload}
            className="inline-flex justify-center px-6 py-2 border border-transparent shadow-sm 
              text-base font-medium rounded-md text-white bg-linkedin-blue 
              hover:bg-linkedin-darker focus:outline-none focus:ring-2 
              focus:ring-offset-2 focus:ring-linkedin-blue transition-colors sm:mt-6"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download
          </button>
        </div>
      </div>
      
      <div className="relative">
        {showLeftScroll && (
          <button
            onClick={() => scroll(-1)}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white/80 p-1 rounded-full shadow-md hover:bg-white"
          >
            <svg className="w-6 h-6 text-linkedin-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        )}
        
        <div
          ref={scrollContainerRef}
          className="flex overflow-x-auto no-scrollbar scroll-smooth gap-2 px-8"
        >
          {Object.keys(visibleSections).map(section => (
            profile[section] && (
              <div key={section} className="flex-shrink-0 flex items-center bg-gray-50 rounded-full px-3 py-1">
                <input
                  type="checkbox"
                  checked={visibleSections[section]}
                  onChange={(e) => setVisibleSections(prev => ({
                    ...prev,
                    [section]: e.target.checked
                  }))}
                  className="mr-2"
                />
                <button
                  onClick={() => onSectionScroll(section)}
                  className="capitalize whitespace-nowrap"
                >
                  {section}
                </button>
                <button
                  onClick={() => onSectionCopy(section)}
                  className="ml-2 text-linkedin-blue hover:text-blue-700"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                  </svg>
                </button>
              </div>
            )
          ))}
        </div>

        {showRightScroll && (
          <button
            onClick={() => scroll(1)}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white/80 p-1 rounded-full shadow-md hover:bg-white"
          >
            <svg className="w-6 h-6 text-linkedin-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}

export default RibbonBar;