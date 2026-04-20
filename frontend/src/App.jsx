import { useState } from 'react';
import Auth from './pages/Auth';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Search from './pages/Search';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [activeTab, setActiveTab] = useState('dashboard');

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  if (!token) {
    return <Auth setToken={setToken} />;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl animate-fade-in">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-accent-primary to-accent-secondary" style={{ display: 'inline-block' }}>
          FINVISION
        </h1>
        <p className="mt-4 text-text-secondary mx-auto" style={{ maxWidth: '600px' }}>
          Next-Generation Multimodal AI Analyst and Enterprise Document Repository.
        </p>
      </header>

      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        onLogout={handleLogout} 
      />

      <main>
        {activeTab === 'dashboard' ? <Dashboard /> : <Search />}
      </main>

      <footer className="mt-20 py-8 text-center text-text-secondary" style={{ fontSize: '0.75rem', opacity: 0.5, borderTop: '1px solid rgba(255,255,255,0.05)' }}>
        © 2026 Financial Document Management System. Built with Gemini 1.5 & FastAPI.
      </footer>
    </div>
  );
}

export default App;
