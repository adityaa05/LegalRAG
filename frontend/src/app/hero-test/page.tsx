import LegalPillNav from '@/components/LegalPillNav'
import DarkVeil from '@/components/DarkVeil'
import HeroSection from '@/components/HeroSection'

export default function HeroTest() {
  return (
    <div className="relative min-h-screen">
      {/* Animated Background - Full Coverage */}
      <div className="fixed inset-0 w-full h-full z-0">
        <DarkVeil 
          hueShift={240}
          noiseIntensity={0.015}
          scanlineIntensity={0.05}
          speed={0.2}
          scanlineFrequency={0.3}
          warpAmount={0.05}
          resolutionScale={0.7}
        />
      </div>

      {/* Content Overlay */}
      <div className="relative z-10">
        <LegalPillNav />
        
        {/* Hero Section - Updated Layout */}
        <HeroSection />
        
        {/* Test Content Below */}
        <div className="min-h-screen bg-black/20 backdrop-blur-sm p-8">
          <div className="max-w-4xl mx-auto text-center text-white">
            <h2 className="text-3xl font-bold mb-6">Hero Section Test Page</h2>
            <div className="space-y-4 text-white/80">
              <p>✅ Background should cover the entire page</p>
              <p>✅ Title "Welcome to KnowYourCrime" should be on one line, centered</p>
              <p>✅ Subtitle "AI-Powered Legal Research Assistant" should be centered below</p>
              <p>✅ Description line should be removed</p>
              <p>✅ Four pill buttons should be centered at the bottom of hero section</p>
              <p>✅ Font sizes should be smaller and more appropriate</p>
            </div>
            
            <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-3">Layout Changes</h3>
                <ul className="text-sm text-white/70 space-y-2 text-left">
                  <li>• Reduced font sizes for better proportions</li>
                  <li>• Centered title and subtitle layout</li>
                  <li>• Removed description text</li>
                  <li>• Moved pill buttons to bottom</li>
                </ul>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-3">Background Fixes</h3>
                <ul className="text-sm text-white/70 space-y-2 text-left">
                  <li>• Fixed background coverage issues</li>
                  <li>• Added proper CSS resets</li>
                  <li>• Ensured full page coverage</li>
                  <li>• Improved canvas sizing</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
