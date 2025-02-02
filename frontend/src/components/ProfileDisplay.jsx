import React, { useState, useRef, useEffect, useCallback } from 'react';
import RibbonBar from './RibbonBar';

function ProfileDisplay({ profile }) {
  const [visibleSections, setVisibleSections] = useState({
    summary: true,
    experience: true,
    education: true,
    honors: true,
    certifications: true,
    projects: true,
    volunteer: true,
    publications: true,
    skills: true,
    languages: true,
    posts: true
  });

  // Refs for section scrolling
  const textareaRef = useRef(null);
  const sectionRefs = useRef({});
  const lineHeightRef = useRef(null);

  // Helper function to copy text to clipboard
  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      // Could add toast notification here
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  // Generate section content for display
  const getSectionContent = (section) => {
    return profile[section] || '';
  };

  // Get full profile text
  const getFullProfileText = () => {
    return Object.keys(visibleSections)
      .filter(section => visibleSections[section] && profile[section])
      .map(section => profile[section])
      .join('\n\n---\n\n');
  };

  // Handle downloading profile as text file
  const downloadAsText = () => {
    const element = document.createElement('a');
    const file = new Blob([getFullProfileText()], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = `${profile.full_name.replace(/\s+/g, '_')}_profile.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  // Calculate section positions whenever visible sections change
  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    let currentPosition = 0;
    const positions = {};
    
    Object.keys(visibleSections)
      .filter(section => visibleSections[section] && profile[section])
      .forEach(section => {
        positions[section] = currentPosition;
        currentPosition += profile[section].split('\n').length;
      });

    sectionRefs.current = positions;
  }, [visibleSections, profile]);

  const calculateLineHeight = useCallback(() => {
    const textarea = textareaRef.current;
    if (!textarea || lineHeightRef.current) return;

    // Create temporary div to measure single line
    const tempDiv = document.createElement('div');
    tempDiv.style.position = 'absolute';
    tempDiv.style.visibility = 'hidden';
    tempDiv.style.height = 'auto';
    tempDiv.style.width = textarea.clientWidth + 'px';
    tempDiv.style.font = window.getComputedStyle(textarea).font;
    tempDiv.innerText = 'George';

    document.body.appendChild(tempDiv);
    const singleLineHeight = tempDiv.clientHeight;
    document.body.removeChild(tempDiv);

    lineHeightRef.current = singleLineHeight;
  }, []);

  // Calculate line height on mount and window resize
  useEffect(() => {
    calculateLineHeight();
    window.addEventListener('resize', calculateLineHeight);
    return () => window.removeEventListener('resize', calculateLineHeight);
  }, [calculateLineHeight]);

  const scrollToSection = useCallback((section) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const position = sectionRefs.current[section];
    if (position !== undefined) {
      // Get actual line height or fall back to estimate
      const lineHeight = lineHeightRef.current || 20;
      const padding = parseInt(window.getComputedStyle(textarea).paddingTop);
      
      textarea.style.scrollBehavior = 'smooth';
      textarea.scrollTop = (position * lineHeight) + padding;
      
      setTimeout(() => {
        textarea.style.scrollBehavior = 'auto';
      }, 1000);
    }
  }, []);

  const handleSectionCopy = (section) => {
    copyToClipboard(getSectionContent(section));
  };

  return (
    <div className="profile-container max-w-4xl mx-auto">
      <RibbonBar
        profile={profile}
        visibleSections={visibleSections}
        setVisibleSections={setVisibleSections}
        onCopyAll={() => copyToClipboard(getFullProfileText())}
        onDownload={downloadAsText}
        onSectionCopy={handleSectionCopy}
        onSectionScroll={scrollToSection}
      />

      <div className="mt-4 bg-white rounded-lg p-6">
        <textarea
          ref={textareaRef}
          value={getFullProfileText()}
          className="w-full h-[600px] font-mono text-sm bg-gray-50 p-4 rounded-md border border-gray-200 focus:border-linkedin-blue focus:ring-linkedin-blue"
        />
      </div>
    </div>
  );
}

export default ProfileDisplay;
