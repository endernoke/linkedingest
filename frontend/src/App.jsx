import React from 'react';
import { Helmet } from 'react-helmet';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { BackendProvider } from './context/BackendContext';
import SearchForm from './components/SearchForm';
import ProfilePage from './components/ProfilePage';
import Welcome from './components/Welcome';
import Footer from './components/Footer';
import ServiceStatus from './components/ServiceStatus';
import NotFound from './components/NotFound';

function App() {
  return (
    <BrowserRouter>
      <BackendProvider>
        <div className="min-h-screen bg-gray-50">
          <Helmet>
            <title>Linkedingest</title>
            <meta name="description" content="Transform LinkedIn profiles into prompt-ready data" />
          </Helmet>
          <header className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
              <a href="/">
                <h1 className="text-3xl font-bold text-linkedin-blue">
                  Linkedingest
                </h1>
              </a>
            </div>
          </header>
          <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
            <ServiceStatus />
            <SearchForm />
            <Routes>
              <Route path="/" element={<Welcome />} />
              <Route path="/in/*" element={<ProfilePage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BackendProvider>
    </BrowserRouter>
  );
}

export default App;