import DarkVeil from '@/components/DarkVeil'
import LegalPillNav from '@/components/LegalPillNav'

export default function BackgroundVariations() {
  const variations = [
    {
      name: "Legal Blue (Default)",
      settings: {
        hueShift: 240,
        noiseIntensity: 0.015,
        scanlineIntensity: 0.05,
        speed: 0.2,
        warpAmount: 0.05
      },
      description: "Professional blue theme optimized for legal research"
    },
    {
      name: "Deep Purple",
      settings: {
        hueShift: 280,
        noiseIntensity: 0.02,
        scanlineIntensity: 0.08,
        speed: 0.15,
        warpAmount: 0.08
      },
      description: "Rich purple with enhanced scanlines for premium feel"
    },
    {
      name: "Emerald Justice",
      settings: {
        hueShift: 120,
        noiseIntensity: 0.01,
        scanlineIntensity: 0.03,
        speed: 0.25,
        warpAmount: 0.03
      },
      description: "Green theme representing justice and balance"
    },
    {
      name: "Crimson Authority",
      settings: {
        hueShift: 0,
        noiseIntensity: 0.025,
        scanlineIntensity: 0.1,
        speed: 0.3,
        warpAmount: 0.1
      },
      description: "Bold red theme for high-impact legal presentations"
    }
  ]

  return (
    <div className="relative min-h-screen">
      <LegalPillNav />
      
      <div className="pt-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-white mb-4">Background Variations</h1>
            <p className="text-xl text-white/80">Different themes for your Legal RAG System</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {variations.map((variation, index) => (
              <div key={index} className="relative">
                {/* Background Preview */}
                <div className="relative h-64 rounded-xl overflow-hidden border-2 border-white/20">
                  <DarkVeil 
                    {...variation.settings}
                    resolutionScale={0.6}
                  />
                  
                  {/* Overlay Info */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end">
                    <div className="p-4 text-white">
                      <h3 className="text-lg font-semibold mb-1">{variation.name}</h3>
                      <p className="text-sm text-white/80">{variation.description}</p>
                    </div>
                  </div>
                </div>

                {/* Settings Display */}
                <div className="mt-4 bg-black/20 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                  <h4 className="text-white font-medium mb-2">Settings:</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm text-white/70">
                    <div>Hue: {variation.settings.hueShift}°</div>
                    <div>Speed: {variation.settings.speed}x</div>
                    <div>Noise: {variation.settings.noiseIntensity}</div>
                    <div>Warp: {variation.settings.warpAmount}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Usage Instructions */}
          <div className="mt-12 bg-black/30 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
            <h2 className="text-2xl font-bold text-white mb-4">How to Use</h2>
            <div className="text-white/80 space-y-4">
              <p>
                The DarkVeil component creates a neural network-inspired animated background 
                perfect for modern legal applications. Each variation is optimized for different 
                use cases and brand aesthetics.
              </p>
              
              <div className="bg-black/40 rounded-lg p-4 font-mono text-sm text-green-300">
                <pre>{`// Example usage with custom settings
<DarkVeil 
  hueShift={240}        // 0-360 degrees
  noiseIntensity={0.02} // 0-0.1 recommended
  scanlineIntensity={0.05} // 0-0.2 for effect
  speed={0.2}           // 0.1-1.0 animation speed
  warpAmount={0.05}     // 0-0.2 distortion
  resolutionScale={0.7} // 0.5-1.0 performance
/>`}</pre>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                <div>
                  <h3 className="font-semibold text-white mb-2">Performance Tips:</h3>
                  <ul className="space-y-1 text-sm">
                    <li>• Use resolutionScale 0.5-0.8 for mobile</li>
                    <li>• Lower speed values reduce CPU usage</li>
                    <li>• Minimal noise/warp for better performance</li>
                    <li>• Consider user motion preferences</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-white mb-2">Design Guidelines:</h3>
                  <ul className="space-y-1 text-sm">
                    <li>• Blue (240°) for professional legal themes</li>
                    <li>• Green (120°) for environmental/justice law</li>
                    <li>• Purple (280°) for premium/corporate law</li>
                    <li>• Red (0°) for criminal/urgent legal matters</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Default background for the page */}
      <div className="fixed inset-0 z-0">
        <DarkVeil 
          hueShift={260}
          noiseIntensity={0.01}
          scanlineIntensity={0.02}
          speed={0.1}
          warpAmount={0.02}
          resolutionScale={0.6}
        />
      </div>
    </div>
  )
}
