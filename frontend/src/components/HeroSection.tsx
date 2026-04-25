'use client'

import React from 'react'
import BlurText from './BlurText'
import PillButton from './PillButton'
import { Scale, ChevronDown } from 'lucide-react'

const HeroSection = () => {
  const handleAnimationComplete = () => {
    console.log('Hero animation completed!');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-between relative px-2 sm:px-4 py-16 sm:py-20">
      {/* Hero Content - Centered */}
      <div className="flex-1 flex flex-col items-center justify-center text-center max-w-4xl mx-auto w-full">
        {/* Logo/Icon */}
        <div className="mb-8">
          <div className="bg-white/10 backdrop-blur-sm rounded-full p-6 border border-white/20">
            <Scale className="h-16 w-16 text-white" />
          </div>
        </div>

        {/* Main Title - Centered on one line */}
        <div className="mb-3 w-full flex justify-center items-center px-4">
          <div className="text-center whitespace-nowrap overflow-hidden">
            <BlurText
              text="KnowYourCrime"
              delay={100}
              animateBy="words"
              direction="top"
              onAnimationComplete={handleAnimationComplete}
              className="text-[clamp(2rem,6vw,5rem)] text-white leading-tight font-duru-sans font-bold"
            />
          </div>
        </div>

        {/* Subtitle - Properly Centered */}
        <div className="mb-12 w-full flex justify-center px-4">
          <div className="text-center">
            <BlurText
              text="Intelligent Legal Search & Analysis"
              delay={150}
              animateBy="words"
              direction="top"
              className="text-[clamp(1rem,2.5vw,1.8rem)] text-white/80 font-almarai"
            />
          </div>
        </div>
      </div>

      {/* Feature Pills - Moved up to avoid overlap */}
      <div className="flex flex-wrap justify-center gap-2 sm:gap-4 mb-8 px-4">
        {[
          "615 IPC Sections",
          "295 Constitutional Articles", 
          "AI-Powered Search",
          "Real-time Analysis"
        ].map((feature, index) => (
          <div key={feature} style={{ animationDelay: `${300 + (index * 100)}ms` }} className="flex-shrink-0">
            <PillButton>
              {feature}
            </PillButton>
          </div>
        ))}
      </div>

      {/* Scroll Indicator - More space from pills */}
      <div className="flex flex-col items-center text-white/60 mt-8">
        <span className="text-sm mb-2 font-medium">Scroll to explore</span>
        <ChevronDown className="h-6 w-6 animate-bounce" />
      </div>
    </div>
  )
}

export default HeroSection
