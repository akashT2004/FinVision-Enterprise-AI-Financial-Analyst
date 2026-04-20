import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  LineChart, Line, PieChart, Pie, Cell, Legend 
} from 'recharts';
import { TrendingUp, PieChart as PieIcon, BarChart3, Quote, Layers } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const COLORS = ['#6366f1', '#0ea5e9', '#10b981', '#f59e0b', '#ec4899'];

export default function InsightPanel({ data, type, answer, citations }) {
  if (!answer && !data) return null;

  // Process data for multi-series support
  const processedData = React.useMemo(() => {
    if (!data || data.length === 0) return [];
    
    // Check if the first item has the 'values' dictionary (multi-series)
    const hasMultipleValues = data[0].values && typeof data[0].values === 'object';
    
    if (hasMultipleValues) {
      // Flatten the values for Recharts: { label: '2023', 'Net Sales': 100, 'Profit': 20 }
      return data.map(item => ({
        label: item.label,
        ...item.values
      }));
    }
    
    // Fallback to single value
    return data;
  }, [data]);

  // Extract keys for multi-series bars/lines
  const seriesKeys = React.useMemo(() => {
    if (data && data.length > 0 && data[0].values) {
      return Object.keys(data[0].values);
    }
    return ['value'];
  }, [data]);

  return (
    <AnimatePresence mode="wait">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="space-y-6 flex flex-col h-full"
      >
        {/* Narrative Answer Card */}
        <div className="glass-card p-6 border-l-4 border-l-accent-primary">
          <div className="flex items-center space-x-2 text-accent-primary mb-4">
            <TrendingUp size={20} />
            <h3 className="text-lg font-bold tracking-tight">AI Analytical Intelligence</h3>
          </div>
          <div className="text-text-primary leading-relaxed text-lg font-light tracking-wide whitespace-pre-wrap">
            {answer}
          </div>
        </div>

        {/* Chart Section */}
        {processedData.length > 0 && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="glass-card p-6 flex-grow min-h-[450px] relative"
          >
            <div className="flex justify-between items-center mb-8">
              <div className="flex items-center space-x-2 text-accent-secondary">
                {type === 'pie' ? <PieIcon size={20} /> : <BarChart3 size={20} />}
                <span className="font-bold text-sm uppercase tracking-widest">Financial Visualization</span>
              </div>
              <div className="flex items-center space-x-1 text-[10px] bg-white/5 border border-white/10 px-2 py-1 rounded-full text-text-secondary">
                <Layers size={10} />
                <span>Multi-Metric Sync</span>
              </div>
            </div>
            
            <div className="h-[320px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                {type === 'bar' ? (
                  <BarChart data={processedData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#2D2D2D" vertical={false} />
                    <XAxis dataKey="label" stroke="#475569" fontSize={11} tickMargin={10} axisLine={false} />
                    <YAxis stroke="#475569" fontSize={11} axisLine={false} tickLine={false} />
                    <Tooltip 
                      cursor={{ fill: 'rgba(255,255,255,0.03)' }}
                      contentStyle={{ 
                        backgroundColor: 'rgba(13, 17, 23, 0.9)', 
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '12px',
                        backdropFilter: 'blur(10px)',
                        boxShadow: '0 10px 20px rgba(0,0,0,0.4)'
                      }}
                    />
                    <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px' }} />
                    {seriesKeys.map((key, index) => (
                      <Bar 
                        key={key} 
                        dataKey={key} 
                        fill={COLORS[index % COLORS.length]} 
                        radius={[6, 6, 0, 0]} 
                        barSize={seriesKeys.length > 1 ? 25 : 45}
                      />
                    ))}
                  </BarChart>
                ) : type === 'pie' ? (
                  <PieChart>
                    <Pie
                      data={processedData}
                      cx="50%"
                      cy="50%"
                      innerRadius={70}
                      outerRadius={100}
                      paddingAngle={8}
                      dataKey={seriesKeys[0]} // Pie usually only supports one metric logically
                    >
                      {processedData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="rgba(0,0,0,0.2)" />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                ) : (
                  <LineChart data={processedData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#2D2D2D" vertical={false} />
                    <XAxis dataKey="label" stroke="#475569" fontSize={11} axisLine={false} />
                    <YAxis stroke="#475569" fontSize={11} axisLine={false} tickLine={false} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(13, 17, 23, 0.9)', 
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '12px'
                      }}
                    />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    {seriesKeys.map((key, index) => (
                      <Line 
                        key={key} 
                        type="monotone" 
                        dataKey={key} 
                        stroke={COLORS[index % COLORS.length]} 
                        strokeWidth={4} 
                        dot={{ r: 4, strokeWidth: 2, fill: '#030508' }} 
                        activeDot={{ r: 8, strokeWidth: 0 }}
                      />
                    ))}
                  </LineChart>
                )}
              </ResponsiveContainer>
            </div>
          </motion.div>
        )}

        {/* Citations Card */}
        {citations && citations.length > 0 && (
          <div className="glass-card p-5 bg-gradient-to-br from-white/5 to-transparent">
            <div className="flex items-center space-x-2 text-text-secondary mb-4">
              <Quote size={16} />
              <h4 className="text-xs font-bold uppercase tracking-widest">Document Evidence</h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {citations.map((c, i) => (
                <div 
                  key={i} 
                  className="group relative cursor-help text-[10px] bg-white/5 hover:bg-accent-primary/10 text-text-secondary hover:text-accent-primary px-3 py-1.5 rounded-lg border border-white/5 transition-all duration-300"
                  title={c.content_snippet}
                >
                  <span className="font-mono">Ref: {c.doc_id.slice(0, 8)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
