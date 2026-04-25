import LegalNavigation from '@/components/LegalNavigation'

export default function NavigationDemo() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <LegalNavigation />
      
      {/* Demo Content */}
      <div className="pt-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">
            Legal RAG Navigation Demo
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Click the menu button (☰) to see the animated card navigation in action
          </p>
          
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Navigation Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
              <div>
                <h3 className="font-semibold text-blue-600 mb-2">🎨 Animated Cards</h3>
                <p className="text-gray-600">GSAP-powered smooth animations with staggered card reveals</p>
              </div>
              <div>
                <h3 className="font-semibold text-green-600 mb-2">📱 Responsive Design</h3>
                <p className="text-gray-600">Desktop horizontal nav, mobile full-screen overlay</p>
              </div>
              <div>
                <h3 className="font-semibold text-purple-600 mb-2">⚖️ Legal-Themed</h3>
                <p className="text-gray-600">Tailored for legal research with proper categorization</p>
              </div>
              <div>
                <h3 className="font-semibold text-red-600 mb-2">🔍 Smart Organization</h3>
                <p className="text-gray-600">Organized by function: Search, Documents, Analytics, etc.</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Navigation Structure</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 text-sm">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">Search</h4>
                <ul className="text-blue-600 space-y-1">
                  <li>• AI Legal Search</li>
                  <li>• Quick Search</li>
                  <li>• Advanced Filters</li>
                  <li>• Search History</li>
                </ul>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-semibold text-green-800 mb-2">Documents</h4>
                <ul className="text-green-600 space-y-1">
                  <li>• IPC (615 sections)</li>
                  <li>• Constitution (295)</li>
                  <li>• CrPC, CPC</li>
                  <li>• Evidence Act</li>
                  <li>• Companies Act</li>
                  <li>• Income Tax Act</li>
                </ul>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-800 mb-2">Analytics</h4>
                <ul className="text-purple-600 space-y-1">
                  <li>• Legal Insights</li>
                  <li>• Usage Statistics</li>
                  <li>• Offense Trends</li>
                  <li>• Document Coverage</li>
                </ul>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <h4 className="font-semibold text-red-800 mb-2">Resources</h4>
                <ul className="text-red-600 space-y-1">
                  <li>• Legal Categories</li>
                  <li>• Punishment Guide</li>
                  <li>• Case References</li>
                  <li>• Legal Glossary</li>
                </ul>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-semibold text-gray-800 mb-2">About</h4>
                <ul className="text-gray-600 space-y-1">
                  <li>• About Legal RAG</li>
                  <li>• How It Works</li>
                  <li>• Data Sources</li>
                  <li>• API Docs</li>
                  <li>• Support</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
