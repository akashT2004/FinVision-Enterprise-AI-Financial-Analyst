import { useState } from 'react';
import api from '../api';
import { 
  Search as SearchIcon, Cpu, ChevronRight, BarChart3, 
  MessageSquare, History, Sparkles, AlertCircle 
} from 'lucide-react';
import InsightPanel from '../components/InsightPanel';
import { motion, AnimatePresence } from 'framer-motion';

export default function Search() {
  const [query, setQuery] = useState('');
  const [analystResponse, setAnalystResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('agent'); // 'agent' or 'search'
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState(null);

  const handleAction = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setAnalystResponse(null);
    setSearchResults([]);
    setError(null);

    try {
      if (mode === 'agent') {
        const { data } = await api.post('/rag/ask', { query });
        setAnalystResponse(data);
      } else {
        const { data } = await api.post('/rag/search', { query });
        setSearchResults(data);
      }
    } catch (err) {
      console.error('Request failed:', err);
      const msg = err.response?.data?.detail || 'The AI Analyst encountered an error. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-8 animate-fade-in">
      {/* Search Header / Mode Toggle */}
      <div className="flex justify-between items-center glass-card p-3 px-6">
        <div className="tab-container">
          <button 
            onClick={() => setMode('agent')}
            className={`tab-btn flex items-center gap-2 ${mode === 'agent' ? 'active' : ''}`}
          >
            <Cpu size={14} />
            <span>AI Analyst Agent</span>
          </button>
          <button 
            onClick={() => setMode('search')}
            className={`tab-btn flex items-center gap-2 ${mode === 'search' ? 'active' : ''}`}
          >
            <SearchIcon size={14} />
            <span>Document Search</span>
          </button>
        </div>
        <div className="flex items-center gap-2 text-[10px] font-bold uppercase opacity-30 tracking-widest hidden md:flex">
          <History size={12} /> Live Session Active
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-8 items-start">
        {/* Interaction Panel */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-sm font-bold uppercase tracking-widest flex items-center gap-2">
                <MessageSquare size={16} className="text-accent-primary" />
                <span>Analytical Core</span>
              </h3>
              <Sparkles size={14} className="opacity-30" />
            </div>
            
            <form onSubmit={handleAction} className="space-y-4">
              <textarea 
                rows={4}
                placeholder={mode === 'agent' ? "Ask specifically about sales, profit, or risk factors..." : "Search for keywords in the index..."}
                className="input-field" style={{ resize: 'none' }}
                value={query}
                onChange={e => setQuery(e.target.value)}
              />
              <button disabled={loading} className="btn-primary w-full shadow-lg shadow-accent-primary/20">
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin h-4 w-4 border-2 border-white/30 border-t-white rounded-full" />
                    <span>Processing Pipeline...</span>
                  </div>
                ) : (
                  <>
                    <span>Run {mode === 'agent' ? 'Deep Analysis' : 'Global Search'}</span>
                    <ChevronRight size={18} />
                  </>
                )}
              </button>
            </form>
          </div>

          <div className="glass-card p-6">
            <h4 className="text-[10px] font-bold uppercase tracking-widest opacity-30 mb-4 border-b border-white/5 pb-2">AI Suggestions</h4>
            <div className="flex flex-col gap-2">
              {[
                "Extract Net Sales for the last 3 years.",
                "Identify internal and external risk factors.",
                "Compare EBITDA against company milestones."
              ].map((s, i) => (
                <button 
                  key={i} onClick={() => setQuery(s)}
                  className="text-left text-xs p-3 glass-card bg-white/5 border-none hover:bg-white/10 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Intelligence Panel (Output) */}
        <div className="lg:col-span-8 h-full">
          {error ? (
            <div className="glass-card p-12 text-center flex flex-col items-center border-accent-primary/30">
              <AlertCircle size={48} className="text-accent-primary opacity-50 mb-4" />
              <h3 className="text-xl font-bold mb-2">Analysis Interrupted</h3>
              <p className="text-sm opacity-50 max-w-sm">{error}</p>
            </div>
          ) : analystResponse ? (
            <InsightPanel 
              answer={analystResponse.answer}
              data={analystResponse.chart_data}
              type={analystResponse.chart_type}
              citations={analystResponse.citations}
            />
          ) : searchResults.length > 0 ? (
            <div className="flex flex-col gap-4">
              {searchResults.map((res, i) => (
                <div key={i} className="glass-card p-6 border-l-4 border-l-accent-secondary bg-gradient-to-br from-white/5 to-transparent">
                  <div className="flex justify-between mb-3 text-[10px] font-bold uppercase tracking-widest">
                    <span className="text-accent-secondary">{res.metadata.title}</span>
                    <span className="opacity-30">Security Rank: {(res.score * 10).toFixed(1)}</span>
                  </div>
                  <p className="text-sm leading-relaxed font-light opacity-80 italic">"{res.content}"</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="h-[450px] flex flex-col items-center justify-center opacity-10 select-none">
              <BarChart3 size={150} />
              <h3 className="text-2xl font-bold uppercase tracking-[0.4em] mt-6">Awaiting Signal</h3>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
