import LegalPillNav from '@/components/LegalPillNav'
import DarkVeil from '@/components/DarkVeil'
import HeroSection from '@/components/HeroSection'
import ScrollReveal from '@/components/ScrollReveal'
import EnhancedSearchSection from '@/components/EnhancedSearchSection'
import Wireframe from '@/components/Wireframe'
import { SearchProvider } from '@/contexts/SearchContext'

export default function Home() {
  return (
    <SearchProvider>
      <div className="relative w-full">
      {/* Animated Background */}
      <div className="fixed top-0 left-0 w-screen h-screen z-0" style={{ width: '100vw', height: '100vh' }}>
        <DarkVeil 
          hueShift={240} // Blue hue for legal theme
          noiseIntensity={0.015}
          scanlineIntensity={0.05}
          speed={0.5}
          scanlineFrequency={0.3}
          warpAmount={0.05}
          resolutionScale={0.7}
        />
      </div>

      {/* Content Overlay */}
      <div className="relative z-10">
        <LegalPillNav />
        
        {/* Hero Section - Full Screen */}
        <HeroSection />
        
        {/* Main Content - Appears on Scroll */}
        <div className="min-h-screen">
          <ScrollReveal
            baseOpacity={0.1}
            enableBlur={true}
            baseRotation={2}
            blurStrength={8}
            containerClassName="px-4 py-20"
            textClassName="text-white text-center font-dm-serif text-[clamp(20px,5vw,36px)] leading-relaxed px-4"
          >
            Discover the power of AI-driven legal research. Navigate through comprehensive Indian legal documents with intelligent search capabilities and real-time analysis.
          </ScrollReveal>
          
          {/* Enhanced Search Section */}
          <div className="mt-20 px-4">
            <EnhancedSearchSection />
          </div>
          
          {/* Wireframe Content */}
          <div className="mt-8">
            <Wireframe />
          </div>
        </div>
      </div>
    </div>
    </SearchProvider>
  )
}
