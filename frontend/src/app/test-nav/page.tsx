import LegalNavigation from '@/components/LegalNavigation'

export default function TestNavigation() {
  return (
    <div className="min-h-screen bg-gray-100">
      <LegalNavigation />
      
      <div className="pt-20 px-4 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Navigation Test Page</h1>
          
          <div className="space-y-6">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h2 className="text-lg font-semibold text-green-800 mb-2">✅ Desktop Navigation (What you see now)</h2>
              <p className="text-green-700">
                The horizontal navigation bar with Legal RAG logo and menu items is working correctly!
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h2 className="text-lg font-semibold text-blue-800 mb-2">📱 To See Mobile Navigation:</h2>
              <ol className="text-blue-700 space-y-2">
                <li><strong>1.</strong> Resize your browser to mobile width (&lt; 768px)</li>
                <li><strong>2.</strong> Look for the hamburger menu (☰) in the top right</li>
                <li><strong>3.</strong> Click it to see the animated card overlay</li>
              </ol>
            </div>

            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h2 className="text-lg font-semibold text-purple-800 mb-2">🎨 Navigation Features:</h2>
              <ul className="text-purple-700 space-y-1">
                <li>• GSAP-powered smooth animations</li>
                <li>• Color-coded legal categories</li>
                <li>• Responsive design (desktop + mobile)</li>
                <li>• Professional legal branding</li>
                <li>• Full-screen card overlay on mobile</li>
              </ul>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h2 className="text-lg font-semibold text-yellow-800 mb-2">🔧 Quick Test:</h2>
              <p className="text-yellow-700 mb-3">
                Press <kbd className="bg-gray-200 px-2 py-1 rounded">F12</kbd> → Click mobile icon 📱 → Click hamburger menu ☰
              </p>
            </div>
          </div>
        </div>

        {/* Spacer content to show scrolling */}
        <div className="space-y-4">
          {Array.from({ length: 10 }, (_, i) => (
            <div key={i} className="bg-white rounded-lg p-6 shadow">
              <h3 className="text-lg font-semibold mb-2">Test Content {i + 1}</h3>
              <p className="text-gray-600">
                This content helps test the fixed navigation positioning and scrolling behavior.
                The navigation should stay fixed at the top while you scroll.
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
