'use client'

import React from 'react'
import { Search, BookOpen, Scale, BarChart3, FileText, Gavel, Shield, Building, Receipt } from 'lucide-react'
import AIResponseCard from './AIResponseCard'
import { useSearch } from '@/contexts/SearchContext'

const Wireframe = () => {
  const { hasSearched, isLoading, searchQuery } = useSearch();

  // Don't render anything if no search has been performed
  if (!hasSearched) {
    return null;
  }

  return (
    <div className="min-h-screen p-4">
      {/* Note: Navigation is now handled by LegalNavigation component */}


      {/* Main Content Area */}
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar - Collapsible on mobile */}
        <div className="lg:w-80 w-full order-2 lg:order-1">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-2xl">
            <h3 className="font-semibold text-white mb-6 flex items-center font-duru-sans text-lg">
              <BookOpen className="h-5 w-5 mr-2" />
              Documents
            </h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-center justify-between p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10">
                <span className="flex items-center">
                  <FileText className="h-4 w-4 mr-2 text-red-400" />
                  <span className="text-white font-almarai">IPC</span>
                </span>
                <span className="text-white/70 font-almarai">(615)</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10">
                <span className="flex items-center">
                  <Shield className="h-4 w-4 mr-2 text-blue-400" />
                  <span className="text-white font-almarai">Constitution</span>
                </span>
                <span className="text-white/70 font-almarai">(295)</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10">
                <span className="flex items-center">
                  <Gavel className="h-4 w-4 mr-2 text-purple-400" />
                  <span className="text-white font-almarai">CrPC</span>
                </span>
                <span className="text-white/70 font-almarai">(22)</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10">
                <span className="flex items-center">
                  <Scale className="h-4 w-4 mr-2 text-green-400" />
                  <span className="text-white font-almarai">CPC</span>
                </span>
                <span className="text-white/70 font-almarai">(104)</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10">
                <span className="flex items-center">
                  <Building className="h-4 w-4 mr-2 text-indigo-400" />
                  <span className="text-white font-almarai">Companies</span>
                </span>
                <span className="text-white/70 font-almarai">(60)</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10">
                <span className="flex items-center">
                  <Receipt className="h-4 w-4 mr-2 text-yellow-400" />
                  <span className="text-white font-almarai">Income Tax</span>
                </span>
                <span className="text-white/70 font-almarai">(234)</span>
              </div>
            </div>

            <h3 className="font-semibold text-white mb-6 mt-8 flex items-center font-duru-sans text-lg">
              <Scale className="h-5 w-5 mr-2" />
              Categories
            </h3>
            <div className="space-y-2 text-sm">
              {['Homicide', 'Property', 'Violence', 'Sexual', 'Fraud', 'Corruption'].map((category) => (
                <div key={category} className="p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10 text-white font-almarai">
                  {category}
                </div>
              ))}
            </div>

            <h3 className="font-semibold text-white mb-6 mt-8 flex items-center font-duru-sans text-lg">
              <BarChart3 className="h-5 w-5 mr-2" />
              Severity
            </h3>
            <div className="space-y-2 text-sm">
              <div className="p-3 bg-red-500/20 backdrop-blur-sm text-red-300 rounded-lg border border-red-400/20 font-almarai">Severe</div>
              <div className="p-3 bg-orange-500/20 backdrop-blur-sm text-orange-300 rounded-lg border border-orange-400/20 font-almarai">High</div>
              <div className="p-3 bg-yellow-500/20 backdrop-blur-sm text-yellow-300 rounded-lg border border-yellow-400/20 font-almarai">Medium</div>
              <div className="p-3 bg-green-500/20 backdrop-blur-sm text-green-300 rounded-lg border border-green-400/20 font-almarai">Low</div>
            </div>
          </div>
        </div>

        {/* Main Results Panel */}
        <div className="flex-1 order-1 lg:order-2">
          <div className="space-y-12">
            {/* Results Section - Full Width & Centered */}
            <section className="text-center">
              <h2 className="text-3xl font-bold text-white mb-8 font-duru-sans">Results</h2>
              <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-2xl max-w-4xl mx-auto">
                
                {isLoading ? (
                  <div className="text-center space-y-6">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
                    <p className="text-lg text-white/90 font-almarai">
                      Searching for: <strong>"{searchQuery}"</strong>
                    </p>
                    <p className="text-base text-white/70 font-almarai">
                      Analyzing legal documents...
                    </p>
                  </div>
                ) : (
                  <div className="text-center space-y-6">
                    <p className="text-lg text-white/90 font-almarai leading-relaxed">
                      Based on your query about <strong>"{searchQuery}"</strong>, here's what I found:
                    </p>
                    <p className="text-base text-white/80 font-almarai leading-relaxed max-w-3xl mx-auto">
                      Murder is defined under Section 302 of the Indian Penal Code (IPC). It is one of the most serious 
                      offenses under Indian criminal law, punishable by death or life imprisonment.
                    </p>
                    
                    {/* Confidence and Sources Row */}
                    <div className="flex items-center justify-center gap-6 pt-4">
                      <span className="bg-green-500/20 text-green-300 px-4 py-2 rounded-full text-sm border border-green-400/20 font-almarai">
                        Confidence: 95%
                      </span>
                      <span className="text-white/70 text-sm font-almarai">
                        Sources: 3 sections found
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </section>

            {/* Relevant Sections - Responsive Grid */}
            {!isLoading && (
              <section>
                <h2 className="text-3xl font-bold text-white mb-8 font-duru-sans">Relevant Sections</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                
                {/* Section Card 1 */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-2xl hover:bg-white/15 transition-all">
                  <div className="flex items-start justify-between mb-4">
                    <span className="bg-red-500/20 text-red-300 px-3 py-1 rounded-full text-xs border border-red-400/20 font-almarai font-medium">
                      IPC
                    </span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-white mb-3 font-duru-sans">
                    Section 302 - Murder
                  </h3>
                  
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="bg-red-500/20 text-red-300 px-2 py-1 rounded text-xs border border-red-400/20 font-almarai">Severe</span>
                    <span className="bg-gray-500/20 text-gray-300 px-2 py-1 rounded text-xs border border-gray-400/20 font-almarai">Non-bailable</span>
                  </div>
                  
                  <p className="text-sm text-white/80 mb-6 font-almarai leading-relaxed">
                    Whoever commits murder shall be punished with death, or imprisonment for life...
                  </p>
                  
                  <button className="w-full bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 px-4 py-2 rounded-lg text-sm border border-blue-400/20 font-almarai font-medium transition-all">
                    View More
                  </button>
                </div>

                {/* Section Card 2 */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-2xl hover:bg-white/15 transition-all">
                  <div className="flex items-start justify-between mb-4">
                    <span className="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-xs border border-blue-400/20 font-almarai font-medium">
                      Constitution
                    </span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-white mb-3 font-duru-sans">
                    Article 21 - Right to Life
                  </h3>
                  
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-xs border border-blue-400/20 font-almarai">Fundamental Right</span>
                  </div>
                  
                  <p className="text-sm text-white/80 mb-6 font-almarai leading-relaxed">
                    No person shall be deprived of his life or personal liberty except according to procedure...
                  </p>
                  
                  <button className="w-full bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 px-4 py-2 rounded-lg text-sm border border-blue-400/20 font-almarai font-medium transition-all">
                    View More
                  </button>
                </div>

                {/* Section Card 3 */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-2xl hover:bg-white/15 transition-all">
                  <div className="flex items-start justify-between mb-4">
                    <span className="bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-xs border border-purple-400/20 font-almarai font-medium">
                      CrPC
                    </span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-white mb-3 font-duru-sans">
                    Section 100 - Arrest
                  </h3>
                  
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="bg-purple-500/20 text-purple-300 px-2 py-1 rounded text-xs border border-purple-400/20 font-almarai">Procedure</span>
                  </div>
                  
                  <p className="text-sm text-white/80 mb-6 font-almarai leading-relaxed">
                    Save as otherwise provided in this Code, any police officer may arrest without warrant...
                  </p>
                  
                  <button className="w-full bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 px-4 py-2 rounded-lg text-sm border border-blue-400/20 font-almarai font-medium transition-all">
                    View More
                  </button>
                </div>

              </div>
              </section>
            )}
          </div>
        </div>
      </div>

    </div>
  )
}

export default Wireframe
