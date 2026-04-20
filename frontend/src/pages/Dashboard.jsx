import { useState, useEffect } from 'react';
import api from '../api';
import { 
  Upload, FileText, Trash2, Building, Tag, 
  Plus, CheckCircle2, Clock, Search as SearchIcon
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Dashboard() {
  const [docs, setDocs] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [formData, setFormData] = useState({ title: '', company_name: '', document_type: 'report' });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => { fetchDocs(); }, []);

  const fetchDocs = async () => {
    try {
      const { data } = await api.get('/documents');
      setDocs(data);
    } catch (err) { console.error('Error fetching docs:', err); }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    const file = e.target.file.files[0];
    if (!file) return;

    setUploading(true);
    const data = new FormData();
    data.append('file', file);
    data.append('title', formData.title);
    data.append('company_name', formData.company_name);
    data.append('document_type', formData.document_type);

    try {
      await api.post('/documents/upload', data);
      setFormData({ title: '', company_name: '', document_type: 'report' });
      e.target.reset();
      fetchDocs();
    } catch (err) {
      alert('Upload failed: ' + (err.response?.data?.detail || 'Unknown error'));
    } finally {
      setUploading(false);
    }
  };

  const deleteDoc = async (id) => {
    if (!confirm('Permanently remove this asset from the high-security index?')) return;
    try {
      await api.delete(`/documents/${id}`);
      fetchDocs();
    } catch (err) { console.error('Error deleting doc:', err); }
  };

  const filteredDocs = docs.filter(doc => 
    doc.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    doc.company_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex flex-col gap-8">
      {/* Metrics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="glass-card p-6" style={{ borderLeft: '4px solid var(--accent-primary)' }}>
          <div className="text-secondary text-xs uppercase tracking-widest font-bold opacity-50 mb-1">Total Assets</div>
          <div className="text-4xl font-bold">{docs.length} <span className="text-xl font-normal opacity-30">Files</span></div>
        </div>
        <div className="glass-card p-6" style={{ borderLeft: '4px solid var(--accent-success)' }}>
          <div className="text-secondary text-xs uppercase tracking-widest font-bold opacity-50 mb-1">Status</div>
          <div className="text-4xl font-bold">100% <span className="text-xl font-normal opacity-30">Online</span></div>
        </div>
        <div className="glass-card p-6" style={{ borderLeft: '4px solid var(--accent-secondary)' }}>
          <div className="text-secondary text-xs uppercase tracking-widest font-bold opacity-50 mb-1">Sync</div>
          <Clock size={24} className="mb-1 text-accent-secondary" />
          <div className="text-xl font-bold opacity-50">Real-time Data Packets</div>
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-8">
        {/* Left Column: Form */}
        <div className="lg:col-span-4">
          <div className="glass-card p-6" style={{ position: 'sticky', top: '2rem' }}>
            <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
              <Upload size={20} className="text-accent-primary" />
              <span>Ingest Asset</span>
            </h3>
            
            <form onSubmit={handleUpload} className="space-y-4">
              <div>
                <label className="text-xs uppercase font-bold tracking-widest opacity-50 mb-2 block">Asset Title</label>
                <input 
                  type="text" className="input-field" required placeholder="e.g. FY24 Annual Report"
                  value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})}
                />
              </div>
              
              <div>
                <label className="text-xs uppercase font-bold tracking-widest opacity-50 mb-2 block">Issuing Entity</label>
                <input 
                  type="text" className="input-field" required placeholder="e.g. Nestle S.A."
                  value={formData.company_name} onChange={e => setFormData({...formData, company_name: e.target.value})}
                />
              </div>

              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="text-xs uppercase font-bold tracking-widest opacity-50 mb-2 block">Category</label>
                  <select 
                    className="input-field" style={{ appearance: 'none', background: 'rgba(255,255,255,0.05)' }}
                    value={formData.document_type} onChange={e => setFormData({...formData, document_type: e.target.value})}
                  >
                    <option value="report">Report</option>
                    <option value="invoice">Invoice</option>
                    <option value="contract">Contract</option>
                  </select>
                </div>
              </div>

              <div className="py-4 border-y border-white/5 my-4">
                <div className="flex items-center gap-2 text-accent-success text-xs font-bold uppercase mb-2">
                  <CheckCircle2 size={14} /> Auto-Secure Enabled
                </div>
                <input type="file" name="file" accept=".pdf" className="text-xs opacity-50" required />
              </div>

              <button disabled={uploading} className="btn-primary w-full">
                {uploading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin h-4 w-4 border-2 border-white/30 border-t-white rounded-full" />
                    <span>Processing...</span>
                  </div>
                ) : (
                  <>
                    <Plus size={18} />
                    <span>Sync to Repository</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: List */}
        <div className="lg:col-span-8">
          <div className="flex items-center justify-between mb-6 px-2">
            <h3 className="text-xl font-bold tracking-tight">Enterprise Repository</h3>
            <div className="flex items-center bg-white/5 border border-white/10 px-3 py-1.5 rounded-lg">
              <SearchIcon size={14} className="opacity-30 mr-2" />
              <input 
                type="text" placeholder="Filter..." className="bg-transparent border-none outline-none text-xs w-32"
                value={searchTerm} onChange={e => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-4">
            {filteredDocs.length === 0 ? (
              <div className="glass-card p-12 text-center opacity-30 italic">No assets found in current index.</div>
            ) : (
              filteredDocs.map((doc) => (
                <div key={doc.document_id} className="glass-card p-5 flex items-center justify-between group">
                  <div className="flex items-center gap-5">
                    <div className="p-3 rounded-2xl bg-accent-primary/10 text-accent-primary group-hover:scale-110 transition-transform">
                      <FileText size={24} />
                    </div>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-bold text-lg">{doc.title}</h4>
                        <span className="text-[10px] uppercase font-bold text-accent-success bg-accent-success/10 px-2 py-0.5 rounded">Verified</span>
                      </div>
                      <div className="flex items-center gap-4 text-xs opacity-50">
                        <span className="flex items-center gap-1"><Building size={14} /> {doc.company_name}</span>
                        <span className="flex items-center gap-1 font-mono uppercase bg-white/5 px-2 rounded">{doc.document_type}</span>
                      </div>
                    </div>
                  </div>
                  <button 
                    onClick={() => deleteDoc(doc.document_id)}
                    className="p-3 text-text-secondary hover:text-red-400 hover:bg-red-400/10 rounded-xl transition-all"
                  >
                    <Trash2 size={20} />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
