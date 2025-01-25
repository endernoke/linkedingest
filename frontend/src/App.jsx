import React from 'react';
import { Helmet } from 'react-helmet';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchForm from './components/SearchForm';
import ProfilePage from './components/ProfilePage';

function App() {
  return (
    <BrowserRouter>
      <div>
        <Helmet>
          <title>LinkedIn Profile Extractor</title>
          <meta name="description" content="Extract information from LinkedIn profiles easily" />
        </Helmet>
        <header>
          <h1>LinkedIn Profile Extractor</h1>
        </header>
        <main>
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