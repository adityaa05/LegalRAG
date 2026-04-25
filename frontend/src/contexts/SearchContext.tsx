'use client'

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface SearchContextType {
  searchQuery: string;
  hasSearched: boolean;
  isLoading: boolean;
  setSearchQuery: (query: string) => void;
  setHasSearched: (searched: boolean) => void;
  setIsLoading: (loading: boolean) => void;
  performSearch: (query: string) => void;
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

  const performSearch = (query: string) => {
    if (query.trim()) {
      setSearchQuery(query);
      setIsLoading(true);
      setHasSearched(true);
      
      // Simulate API call delay
      setTimeout(() => {
        setIsLoading(false);
      }, 1500);
    }
  };

  const value = {
    searchQuery,
    hasSearched,
    isLoading,
    setSearchQuery,
    setHasSearched,
    setIsLoading,
    performSearch,
  };

  return (
    <SearchContext.Provider value={value}>
      {children}
    </SearchContext.Provider>
  );
};
