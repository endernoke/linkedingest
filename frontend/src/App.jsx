import React from 'react';
import { Helmet } from 'react-helmet';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchForm from './components/SearchForm';
import ProfilePage from './components/ProfilePage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Helmet>
          <title>LinkedIn Profile Extractor</title>
          <meta name="description" content="Extract information from LinkedIn profiles easily" />
        </Helmet>
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold text-linkedin-blue">
              LinkedIn Profile Extractor
            </h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <SearchForm />
          <Routes>
            <Route path="/" element={null} />
            <Route path="/in/:userId" element={<ProfilePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;