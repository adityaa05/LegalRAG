import LegalPillNav from '@/components/LegalPillNav'
import DarkVeil from '@/components/DarkVeil'

export default function PillNavDemo() {
  return (
    <div className="relative min-h-screen">
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
          <div className="max-w-4xl mx-auto text-center text-white">
            <h1 className="text-4xl font-bold mb-6">Pill Navigation Demo</h1>
            <p className="text-xl text-white/80 mb-12">
              Modern pill-style navigation with GSAP animations
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h2 className="text-2xl font-semibold mb-4">Navigation Features</h2>
                <ul className="text-left space-y-2 text-white/80">
                  <li>✨ **Animated pill hover effects** with GSAP</li>
                  <li>🎯 **Logo rotation animation** on hover</li>
                  <li>📱 **Responsive mobile menu** with hamburger</li>
                  <li>🎨 **Semi-transparent design** matching theme</li>
                  <li>⚖️ **Legal branding** with scale icon</li>
                  <li>🔗 **Next.js Link integration** for routing</li>
                </ul>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h2 className="text-2xl font-semibold mb-4">Design Elements</h2>
                <ul className="text-left space-y-2 text-white/80">
                  <li>🎪 **Pill-shaped navigation items**</li>
                  <li>🌊 **Smooth hover animations**</li>
                  <li>💫 **Active state indicators**</li>
                  <li>🎭 **Color-coded interactions**</li>
                  <li>📐 **Perfect alignment and spacing**</li>
                  <li>🎨 **Theme-consistent styling**</li>
                </ul>
              </div>
            </div>

            <div className="bg-black/20 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
              <h2 className="text-2xl font-bold mb-6">Navigation Structure</h2>
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4 text-sm">
                <div className="bg-blue-500/20 backdrop-blur-sm border border-blue-400/30 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-200 mb-2">Home</h3>
                  <p className="text-blue-300/70">Main landing page</p>
                </div>
                <div className="bg-green-500/20 backdrop-blur-sm border border-green-400/30 rounded-lg p-4">
                  <h3 className="font-semibold text-green-200 mb-2">Search</h3>
                  <p className="text-green-300/70">AI legal search</p>
                </div>
                <div className="bg-purple-500/20 backdrop-blur-sm border border-purple-400/30 rounded-lg p-4">
                  <h3 className="font-semibold text-purple-200 mb-2">Documents</h3>
                  <p className="text-purple-300/70">Legal document browser</p>
                </div>
                <div className="bg-yellow-500/20 backdrop-blur-sm border border-yellow-400/30 rounded-lg p-4">
                  <h3 className="font-semibold text-yellow-200 mb-2">Analytics</h3>
                  <p className="text-yellow-300/70">Usage insights</p>
                </div>
                <div className="bg-red-500/20 backdrop-blur-sm border border-red-400/30 rounded-lg p-4">
                  <h3 className="font-semibold text-red-200 mb-2">About</h3>
                  <p className="text-red-300/70">System information</p>
                </div>
              </div>
            </div>

            <div className="mt-12 text-center">
              <p className="text-white/60 mb-4">
                Hover over the navigation items above to see the animations in action!
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <span className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm">
                  GSAP Animations
                </span>
                <span className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm">
                  Responsive Design
                </span>
                <span className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm">
                  Modern UI
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
