import DarkVeil from '@/components/DarkVeil'
import LegalPillNav from '@/components/LegalPillNav'

export default function BackgroundDemo() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 z-0">
        <DarkVeil 
          hueShift={240} // Blue hue for legal theme
          noiseIntensity={0.02}
          scanlineIntensity={0.1}
          speed={0.3}
          scanlineFrequency={0.5}
          warpAmount={0.1}
          resolutionScale={0.8}
        />
      </div>

      {/* Content Overlay */}
      <div className="relative z-10">
        <LegalPillNav />
        
        <div className="pt-20 px-4">
          <div className="max-w-4xl mx-auto">
            {/* Hero Section with Background */}
            <div className="text-center py-20">
              <div className="bg-black/20 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
                <h1 className="text-5xl font-bold text-white mb-6">
                  Legal RAG System
                </h1>
                <p className="text-xl text-white/80 mb-8">
                  AI-Powered Legal Research with Dynamic Background
                </p>
                <div className="flex flex-wrap justify-center gap-4">
                  <div className="bg-blue-500/20 backdrop-blur-sm border border-blue-400/30 rounded-lg px-6 py-3">
                    <span className="text-blue-200 font-medium">Neural Network Visualization</span>
                  </div>
                  <div className="bg-purple-500/20 backdrop-blur-sm border border-purple-400/30 rounded-lg px-6 py-3">
                    <span className="text-purple-200 font-medium">WebGL Powered</span>
                  </div>
                  <div className="bg-green-500/20 backdrop-blur-sm border border-green-400/30 rounded-lg px-6 py-3">
                    <span className="text-green-200 font-medium">Real-time Animation</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Feature Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              {[
                {
                  title: "Dynamic Background",
                  description: "Neural network-inspired animated background using WebGL shaders",
                  color: "blue"
                },
                {
                  title: "Legal Theme",
                  description: "Professional color scheme optimized for legal research interface",
                  color: "purple"
                },
                {
                  title: "Performance Optimized",
                  description: "Efficient rendering with adjustable quality settings",
                  color: "green"
                },
                {
                  title: "Customizable Effects",
                  description: "Adjustable hue shift, noise, scanlines, and warp effects",
                  color: "red"
                },
                {
                  title: "Responsive Design",
                  description: "Adapts to different screen sizes and device capabilities",
                  color: "yellow"
                },
                {
                  title: "Accessibility Ready",
                  description: "Can be disabled for users with motion sensitivity",
                  color: "indigo"
                }
              ].map((feature, index) => (
                <div key={index} className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
                  <h3 className="text-lg font-semibold text-white mb-3">{feature.title}</h3>
                  <p className="text-white/70 text-sm">{feature.description}</p>
                </div>
              ))}
            </div>

            {/* Background Controls */}
            <div className="bg-black/30 backdrop-blur-sm rounded-2xl p-8 border border-white/10 mb-12">
              <h2 className="text-2xl font-bold text-white mb-6">Background Configuration</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-white/80">
                <div>
                  <h3 className="font-semibold text-white mb-2">Current Settings:</h3>
                  <ul className="space-y-1 text-sm">
                    <li>• Hue Shift: 240° (Blue theme)</li>
                    <li>• Noise Intensity: 0.02</li>
                    <li>• Scanline Intensity: 0.1</li>
                    <li>• Animation Speed: 0.3x</li>
                    <li>• Warp Amount: 0.1</li>
                    <li>• Resolution Scale: 0.8x</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-white mb-2">Performance Notes:</h3>
                  <ul className="space-y-1 text-sm">
                    <li>• WebGL 2.0 compatible</li>
                    <li>• 60 FPS target on modern devices</li>
                    <li>• Automatic quality scaling</li>
                    <li>• Memory efficient rendering</li>
                    <li>• Responsive to window resize</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Integration Example */}
            <div className="bg-black/20 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
              <h2 className="text-2xl font-bold text-white mb-4">Integration Code</h2>
              <div className="bg-black/40 rounded-lg p-4 font-mono text-sm text-green-300 overflow-x-auto">
                <pre>{`import DarkVeil from '@/components/DarkVeil'

// Basic usage
<div style={{ width: '100%', height: '600px', position: 'relative' }}>
  <DarkVeil />
</div>

// With custom settings for legal theme
<DarkVeil 
  hueShift={240}        // Blue hue
  noiseIntensity={0.02} // Subtle noise
  speed={0.3}           // Slow animation
  resolutionScale={0.8} // Performance optimization
/>`}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
