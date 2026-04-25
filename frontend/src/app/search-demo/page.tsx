import LegalPillNav from '@/components/LegalPillNav'
import DarkVeil from '@/components/DarkVeil'
import EnhancedSearchSection from '@/components/EnhancedSearchSection'
import AnimatedInput from '@/components/AnimatedInput'
import SpotlightCard from '@/components/SpotlightCard'

export default function SearchDemo() {
  return (
    <div className="relative w-full">
      {/* Animated Background */}
      <div className="fixed top-0 left-0 w-screen h-screen z-0" style={{ width: '100vw', height: '100vh' }}>
        <DarkVeil 
          hueShift={240}
          noiseIntensity={0.015}
          scanlineIntensity={0.05}
          speed={0.2}
          warpAmount={0.05}
          resolutionScale={0.7}
        />
      </div>

      {/* Content Overlay */}
      <div className="relative z-10">
        <LegalPillNav />
        
        <div className="pt-32 px-4">
          <div className="max-w-6xl mx-auto">
            {/* Page Header */}
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-white mb-4 font-ghea-narek">
                Animated Search Components
              </h1>
              <p className="text-xl text-white/80 font-almarai">
                Showcase of the enhanced search interface with animated effects
              </p>
            </div>

            {/* Enhanced Search Section */}
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-white mb-6 text-center font-almarai">
                Glassmorphism Search Interface
              </h2>
              <EnhancedSearchSection />
            </div>

            {/* Standalone Animated Input */}
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-white mb-6 text-center font-almarai">
                Standalone Animated Input
              </h2>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20">
                <div className="flex justify-center">
                  <AnimatedInput />
                </div>
              </div>
            </div>

            {/* Spotlight Cards */}
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-white mb-6 text-center font-almarai">
                Interactive Spotlight Cards
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <SpotlightCard className="p-6" spotlightColor="rgba(59, 130, 246, 0.3)">
                  <div className="text-center">
                    <h3 className="text-white font-semibold mb-2 font-almarai">IPC Sections</h3>
                    <p className="text-white/70 text-sm font-almarai">Indian Penal Code provisions</p>
                  </div>
                </SpotlightCard>
                
                <SpotlightCard className="p-6" spotlightColor="rgba(34, 197, 94, 0.3)">
                  <div className="text-center">
                    <h3 className="text-white font-semibold mb-2 font-almarai">Constitution</h3>
                    <p className="text-white/70 text-sm font-almarai">Constitutional articles and amendments</p>
                  </div>
                </SpotlightCard>
                
                <SpotlightCard className="p-6" spotlightColor="rgba(168, 85, 247, 0.3)">
                  <div className="text-center">
                    <h3 className="text-white font-semibold mb-2 font-almarai">Criminal Procedure</h3>
                    <p className="text-white/70 text-sm font-almarai">CrPC sections and procedures</p>
                  </div>
                </SpotlightCard>
                
                <SpotlightCard className="p-6" spotlightColor="rgba(249, 115, 22, 0.3)">
                  <div className="text-center">
                    <h3 className="text-white font-semibold mb-2 font-almarai">Evidence Act</h3>
                    <p className="text-white/70 text-sm font-almarai">Rules of evidence and proof</p>
                  </div>
                </SpotlightCard>
                
                <SpotlightCard className="p-6" spotlightColor="rgba(236, 72, 153, 0.3)">
                  <div className="text-center">
                    <h3 className="text-white font-semibold mb-2 font-almarai">Companies Act</h3>
                    <p className="text-white/70 text-sm font-almarai">Corporate law and regulations</p>
                  </div>
                </SpotlightCard>
                
                <SpotlightCard className="p-6" spotlightColor="rgba(14, 165, 233, 0.3)">
                  <div className="text-center">
                    <h3 className="text-white font-semibold mb-2 font-almarai">Civil Procedure</h3>
                    <p className="text-white/70 text-sm font-almarai">Civil court procedures</p>
                  </div>
                </SpotlightCard>
              </div>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-3 font-almarai">
                  🌟 Animated Borders
                </h3>
                <p className="text-white/70 font-almarai">
                  Beautiful rotating gradient borders that respond to hover and focus states
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-3 font-almarai">
                  🎨 Gradient Effects
                </h3>
                <p className="text-white/70 font-almarai">
                  Multiple layered gradient effects creating depth and visual interest
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-3 font-almarai">
                  ⚡ Interactive States
                </h3>
                <p className="text-white/70 font-almarai">
                  Smooth transitions between normal, hover, and focus states
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-3 font-almarai">
                  🔍 Search Icons
                </h3>
                <p className="text-white/70 font-almarai">
                  Custom SVG icons with gradient fills and proper positioning
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-3 font-almarai">
                  🎭 Filter Button
                </h3>
                <p className="text-white/70 font-almarai">
                  Animated filter icon with rotating border effects
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-3 font-almarai">
                  💫 Spotlight Effects
                </h3>
                <p className="text-white/70 font-almarai">
                  Interactive spotlight cards with mouse-following radial gradients
                </p>
              </div>
            </div>

            {/* Technical Details */}
            <div className="bg-black/20 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
              <h2 className="text-2xl font-bold text-white mb-6 text-center font-ghea-narek">
                Technical Implementation
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3 font-almarai">
                    Styled Components
                  </h3>
                  <ul className="text-white/70 space-y-2 font-almarai">
                    <li>• CSS-in-JS with styled-components</li>
                    <li>• Complex conic gradients for borders</li>
                    <li>• Multiple layered pseudo-elements</li>
                    <li>• Smooth CSS transitions</li>
                  </ul>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3 font-almarai">
                    Animation Features
                  </h3>
                  <ul className="text-white/70 space-y-2 font-almarai">
                    <li>• Rotating gradient animations</li>
                    <li>• Hover state transformations</li>
                    <li>• Focus-within interactions</li>
                    <li>• Blur and glow effects</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
