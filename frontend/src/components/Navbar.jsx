import { LayoutDashboard, Search, LogOut, Terminal, Shield } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Navbar({ activeTab, setActiveTab, onLogout }) {
  const tabs = [
    { id: 'dashboard', label: 'Documents', icon: LayoutDashboard },
    { id: 'search', label: 'Research Hub', icon: Search },
  ];

  return (
    <motion.nav 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card mb-8 p-3 px-6 flex items-center justify-between relative"
    >
      {/* Branding */}
      <div className="flex items-center space-x-3 group cursor-pointer">
        <div className="w-10 h-10 bg-accent-primary rounded-xl flex items-center justify-center shadow-lg shadow-accent-primary/20 group-hover:scale-110 transition-transform">
          <Shield className="text-white" size={20} fill="currentColor" />
        </div>
        <div className="flex flex-col">
          <span className="text-xl font-bold tracking-tighter leading-none selection:bg-accent-primary">FINVISION</span>
          <span className="text-[10px] text-accent-primary font-bold tracking-[0.2em] opacity-80 uppercase">AI Analyst</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="tab-container">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`tab-btn flex items-center space-x-2 transition-all ${
                activeTab === tab.id ? 'active' : ''
              }`}
            >
              <Icon size={16} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
      
      {/* Action Area */}
      <div className="flex items-center space-x-4">
        <div className="hidden lg:flex items-center space-x-2 text-[10px] text-text-secondary opacity-40 px-3 py-1 border-x border-white/5">
          <Terminal size={12} />
          <span className="font-mono">v1.2 // SECURE</span>
        </div>
        
        <button 
          onClick={onLogout}
          className="flex items-center space-x-2 px-4 py-2 text-text-secondary hover:text-white transition-all text-sm font-medium"
        >
          <LogOut size={16} />
          <span>Exit System</span>
        </button>
      </div>
    </motion.nav>
  );
}
