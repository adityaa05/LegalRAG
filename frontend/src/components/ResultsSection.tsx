'use client'

import React from 'react';
import { useSearch } from '@/contexts/SearchContext';
import SpotlightCard from './SpotlightCard';
import { AlertTriangle, CheckCircle, Info, ShieldAlert } from 'lucide-react';

const ResultsSection = () => {
  const { results, isLoading, hasSearched, error } = useSearch();

  if (!hasSearched && !isLoading) return null;

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto mt-12 px-4">
        <div className="flex flex-col items-center justify-center space-y-4 py-20">
          <div className="relative w-16 h-16">
            <div className="absolute top-0 left-0 w-full h-full border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin"></div>
          </div>
          <p className="text-white/60 font-almarai text-lg">Consulting legal database...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-5xl mx-auto mt-12 px-4">
        <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center">
          <ShieldAlert className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-white font-duru-sans text-lg">{error}</p>
        </div>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="max-w-5xl mx-auto mt-12 px-4">
        <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-12 text-center">
          <Info className="w-12 h-12 text-blue-400 mx-auto mb-4" />
          <p className="text-white font-duru-sans text-xl">No specific legal matches found for your query.</p>
          <p className="text-white/60 mt-2 font-almarai">Try rephrasing your situation with more legal keywords.</p>
        </div>
      </div>
    );
  }

  const getSeverityStyles = (severity: string) => {
    switch (severity.toUpperCase()) {
      case 'RED':
        return {
          bg: 'bg-red-500/10',
          border: 'border-red-500/30',
          text: 'text-red-400',
          icon: <ShieldAlert className="w-5 h-5" />,
          label: 'High Severity'
        };
      case 'YELLOW':
        return {
          bg: 'bg-orange-500/10',
          border: 'border-orange-500/30',
          text: 'text-orange-400',
          icon: <AlertTriangle className="w-5 h-5" />,
          label: 'Moderate Severity'
        };
      case 'GREEN':
        return {
          bg: 'bg-green-500/10',
          border: 'border-green-500/30',
          text: 'text-green-400',
          icon: <CheckCircle className="w-5 h-5" />,
          label: 'Low Severity'
        };
      default:
        return {
          bg: 'bg-blue-500/10',
          border: 'border-blue-500/30',
          text: 'text-blue-400',
          icon: <Info className="w-5 h-5" />,
          label: 'Unknown Severity'
        };
    }
  };

  return (
    <div className="max-w-5xl mx-auto mt-12 px-4 pb-20">
      <h2 className="text-white font-dm-serif text-3xl mb-8 border-l-4 border-blue-500 pl-4">
        Legal Analysis Results
      </h2>
      
      <div className="space-y-6">
        {results.map((result, index) => {
          const styles = getSeverityStyles(result.severity);
          
          return (
            <SpotlightCard 
              key={index} 
              className="p-0 overflow-hidden" 
              spotlightColor="rgba(59, 130, 246, 0.15)"
            >
              <div className="p-6 md:p-8">
                {/* Header: Act & Section */}
                <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
                  <div className="flex items-center space-x-3">
                    <span className="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                      {result.act}
                    </span>
                    <span className="text-white font-bold text-xl font-duru-sans">
                      Section {result.section}
                    </span>
                  </div>
                  
                  <div className={`flex items-center space-x-2 px-4 py-1.5 rounded-lg border ${styles.bg} ${styles.border} ${styles.text}`}>
                    {styles.icon}
                    <span className="text-sm font-bold font-almarai">{styles.label}</span>
                  </div>
                </div>
                
                {/* Section Title */}
                <h3 className="text-blue-400 font-bold text-lg mb-4 font-duru-sans italic">
                  "{result.title}"
                </h3>
                
                {/* Legal Text */}
                <div className="bg-white/5 rounded-xl p-5 mb-6 border border-white/5">
                  <p className="text-white/90 font-almarai leading-relaxed text-lg italic">
                    {result.text}
                  </p>
                </div>
                
                {/* Metadata Badges */}
                <div className="flex flex-wrap gap-2">
                  {result.metadata.bailable && (
                    <div className="bg-white/5 border border-white/10 px-3 py-1 rounded text-xs text-white/70">
                      Bailable: <span className="text-white">{result.metadata.bailable === 'True' ? 'Yes' : 'No'}</span>
                    </div>
                  )}
                  {result.metadata.cognizable && (
                    <div className="bg-white/5 border border-white/10 px-3 py-1 rounded text-xs text-white/70">
                      Cognizable: <span className="text-white">{result.metadata.cognizable === 'True' ? 'Yes' : 'No'}</span>
                    </div>
                  )}
                  {result.metadata.offense_type && (
                    <div className="bg-white/5 border border-white/10 px-3 py-1 rounded text-xs text-white/70">
                      Type: <span className="text-white capitalize">{result.metadata.offense_type}</span>
                    </div>
                  )}
                  {result.metadata.maximum_punishment_years > 0 && (
                    <div className="bg-white/5 border border-white/10 px-3 py-1 rounded text-xs text-white/70">
                      Max Punishment: <span className="text-white">{result.metadata.maximum_punishment_years} Years</span>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Footer: Relevance Score */}
              <div className="bg-white/5 border-t border-white/10 px-8 py-3 flex justify-between items-center">
                <span className="text-white/40 text-xs font-almarai">Semantic Similarity Match</span>
                <div className="w-32 h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-blue-500" 
                    style={{ width: `${result.similarity * 100}%` }}
                  />
                </div>
              </div>
            </SpotlightCard>
          );
        })}
      </div>
      
      {/* Disclaimer */}
      <div className="mt-12 p-6 bg-yellow-500/5 border border-yellow-500/20 rounded-xl">
        <div className="flex items-start space-x-3">
          <ShieldAlert className="w-6 h-6 text-yellow-500 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-yellow-500 font-bold mb-1">Legal Disclaimer</h4>
            <p className="text-white/60 text-sm font-almarai leading-relaxed">
              This application provides AI-assisted legal document retrieval and is NOT a substitute for professional legal advice. 
              Laws and their interpretations change frequently. Always consult with a qualified legal professional for your specific situation.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsSection;
