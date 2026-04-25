'use client'

import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface SearchResult {
  text: string;
  act: string;
  section: string;
  title: string;
  severity: string;
  similarity: float;
  metadata: {
    section_number: string;
    section_title: string;
    offense_type?: string;
    punishment_severity?: string;
    bailable?: string;
    cognizable?: string;
    maximum_punishment_years?: number;
    keywords?: string;
    [key: string]: any;
  };
}

interface SearchContextType {
  searchQuery: string;
  hasSearched: boolean;
  isLoading: boolean;
  results: SearchResult[];
  error: string | null;
  setSearchQuery: (query: string) => void;
  setHasSearched: (searched: boolean) => void;
  setIsLoading: (loading: boolean) => void;
  performSearch: (query: string) => void;
  clearResults: () => void;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export const useSearch = () => {
  const context = useContext(SearchContext);
  if (context === undefined) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
};

interface SearchProviderProps {
  children: ReactNode;
}

export const SearchProvider: React.FC<SearchProviderProps> = ({ children }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [error, setError] = useState<string | null>(null);

  const performSearch = async (query: string) => {
    if (query.trim()) {
      setSearchQuery(query);
      setIsLoading(true);
      setHasSearched(true);
      setError(null);
      
      try {
        const response = await fetch('http://localhost:8001/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: query,
            num_results: 5,
          }),
        });

        if (!response.ok) {
          throw new Error('Search failed');
        }

        const data = await response.json();
        setResults(data.results);
      } catch (err) {
        console.error('Search error:', err);
        setError('Failed to connect to the legal database. Please ensure the backend is running.');
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const clearResults = () => {
    setResults([]);
    setHasSearched(false);
    setError(null);
  };

  const value = {
    searchQuery,
    hasSearched,
    isLoading,
    results,
    error,
    setSearchQuery,
    setHasSearched,
    setIsLoading,
    performSearch,
    clearResults,
  };

  return (
    <SearchContext.Provider value={value}>
      {children}
    </SearchContext.Provider>
  );
};
