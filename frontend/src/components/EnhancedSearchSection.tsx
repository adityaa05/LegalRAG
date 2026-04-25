'use client'

import React from 'react'
import AnimatedInput from './AnimatedInput'
import SpotlightCard from './SpotlightCard'
import { Gavel } from 'lucide-react'

const EnhancedSearchSection = () => {
  return (
    <div className="max-w-5xl mx-auto text-center">
      {/* Search Card with Glassmorphism */}
      <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 mb-8 shadow-2xl">
        {/* Animated Search Input */}
        <div className="mb-8 flex justify-center">
          <AnimatedInput />
        </div>
        
        {/* Stats Cards with Spotlight Effect */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <SpotlightCard className="p-4" spotlightColor="rgba(59, 130, 246, 0.3)">
            <div className="text-center">
              <div className="font-bold text-blue-400 text-xl mb-1 font-duru-sans">615</div>
              <div className="font-almarai text-white/90 text-xs">IPC Sections</div>
            </div>
          </SpotlightCard>
          
          <SpotlightCard className="p-4" spotlightColor="rgba(34, 197, 94, 0.3)">
            <div className="text-center">
              <div className="font-bold text-green-400 text-xl mb-1 font-duru-sans">295</div>
              <div className="font-almarai text-white/90 text-xs">Constitutional Articles</div>
            </div>
          </SpotlightCard>
          
          <SpotlightCard className="p-4" spotlightColor="rgba(168, 85, 247, 0.3)">
            <div className="text-center">
              <div className="font-bold text-purple-400 text-xl mb-1 font-duru-sans">484</div>
              <div className="font-almarai text-white/90 text-xs">CrPC Sections</div>
            </div>
          </SpotlightCard>
          
          <SpotlightCard className="p-4" spotlightColor="rgba(249, 115, 22, 0.3)">
            <div className="text-center">
              <div className="font-bold text-orange-400 text-xl mb-1 font-duru-sans">1000+</div>
              <div className="font-almarai text-white/90 text-xs">Case Studies</div>
            </div>
          </SpotlightCard>
        </div>
      </div>
    </div>
  )
}

export default EnhancedSearchSection
