import LegalPillNav from '@/components/LegalPillNav'
import DarkVeil from '@/components/DarkVeil'
import HeroSection from '@/components/HeroSection'

export default function UpdatedDesign() {
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
        
        {/* Hero Section with New Fonts */}
        <HeroSection />
        
        {/* Demo Content */}
        <div className="min-h-screen bg-black/20 backdrop-blur-sm p-8">
          <div className="max-w-4xl mx-auto text-center text-white">
            <h2 className="text-3xl font-bold mb-6 font-ghea-narek">Updated Design Features</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold mb-4 font-almarai">Typography Updates</h3>
                <ul className="text-left space-y-2 text-white/80 font-almarai">
                  <li>✨ **Title:** GHEA Narek Serif Heavy (fallback: Inter 900)</li>
                  <li>📝 **Subtitle:** Almarai font family</li>
                  <li>🎨 **Professional typography** for legal branding</li>
                  <li>📱 **Responsive font sizing** with clamp()</li>
                </ul>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold mb-4 font-almarai">Navigation Improvements</h3>
                <ul className="text-left space-y-2 text-white/80 font-almarai">
                  <li>🎯 **Centered navigation** with fixed positioning</li>
                  <li>🌙 **Dark mode support** with proper contrast</li>
                  <li>📏 **Better spacing** between nav items</li>
                  <li>🚫 **Logo removed** as requested</li>
                  <li>💫 **Smooth hover animations**</li>
                </ul>
              </div>
            </div>

            <div className="bg-black/20 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
              <h2 className="text-2xl font-bold mb-6 font-ghea-narek">Font Showcase</h2>
              
              <div className="space-y-6">
                <div className="text-center">
                  <h3 className="text-4xl font-ghea-narek text-white mb-2">GHEA Narek Serif Heavy</h3>
                  <p className="text-white/60 font-almarai">Used for main titles and headings</p>
                </div>
                
                <div className="text-center">
                  <h3 className="text-2xl font-almarai text-white mb-2">Almarai Font Family</h3>
                  <p className="text-white/60 font-almarai">Used for subtitles and body text</p>
                </div>
                
                <div className="text-center">
                  <h3 className="text-xl font-bold text-white mb-2">Inter (Fallback)</h3>
                  <p className="text-white/60">Used when GHEA Narek is not available</p>
                </div>
              </div>
            </div>

            <div className="mt-12 text-center">
              <p className="text-white/60 mb-4 font-almarai">
                All improvements implemented as requested!
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <span className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm font-almarai">
                  Custom Fonts
                </span>
                <span className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm font-almarai">
                  Centered Navigation
                </span>
                <span className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm font-almarai">
                  Dark Mode Support
                </span>
                <span className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm font-almarai">
                  Better Spacing
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
