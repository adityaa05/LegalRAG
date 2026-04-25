import LegalPillNav from '@/components/LegalPillNav'
import DarkVeil from '@/components/DarkVeil'
import HeroSection from '@/components/HeroSection'
import ScrollReveal from '@/components/ScrollReveal'
import BlurText from '@/components/BlurText'

export default function HeroDemo() {
  return (
    <div className="relative">
      {/* Animated Background */}
      <div className="fixed inset-0 z-0">
        <DarkVeil 
          hueShift={240}
          noiseIntensity={0.02}
          scanlineIntensity={0.08}
          speed={0.25}
          warpAmount={0.08}
          resolutionScale={0.8}
        />
      </div>

      {/* Content Overlay */}
      <div className="relative z-10">
        <LegalPillNav />
        
        {/* Hero Section */}
        <HeroSection />
        
        {/* Scroll Content Sections */}
        <div className="space-y-32 pb-20">
          
          {/* Section 1 */}
          <ScrollReveal
            baseOpacity={0.1}
            enableBlur={true}
            baseRotation={3}
            blurStrength={10}
            containerClassName="px-4"
            textClassName="text-white text-center max-w-4xl mx-auto"
          >
            KnowYourCrime revolutionizes legal research by combining artificial intelligence with comprehensive Indian legal databases, making complex legal information accessible to everyone.
          </ScrollReveal>

          {/* Section 2 */}
          <ScrollReveal
            baseOpacity={0.1}
            enableBlur={true}
            baseRotation={-2}
            blurStrength={8}
            containerClassName="px-4"
            textClassName="text-white text-center max-w-4xl mx-auto"
          >
            From the Indian Penal Code to Constitutional Articles, our platform provides intelligent search across 615 IPC sections, 295 constitutional articles, and comprehensive legal procedures.
          </ScrollReveal>

          {/* Section 3 */}
          <ScrollReveal
            baseOpacity={0.1}
            enableBlur={true}
            baseRotation={2}
            blurStrength={12}
            containerClassName="px-4"
            textClassName="text-white text-center max-w-4xl mx-auto"
          >
            Experience the future of legal research with real-time AI analysis, contextual understanding, and instant access to relevant legal precedents and procedures.
          </ScrollReveal>

          {/* Feature Grid */}
          <div className="px-4 max-w-6xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[
                {
                  title: "Smart Legal Search",
                  description: "AI-powered search that understands legal context and provides relevant results instantly"
                },
                {
                  title: "Comprehensive Database",
                  description: "Access to complete Indian legal documents including IPC, Constitution, and procedural codes"
                },
                {
                  title: "Real-time Analysis",
                  description: "Get instant analysis of legal sections with punishment details and case relevance"
                },
                {
                  title: "Interactive Interface",
                  description: "Modern, intuitive design that makes complex legal research simple and efficient"
                },
                {
                  title: "Cross-referencing",
                  description: "Intelligent linking between related legal sections and constitutional provisions"
                },
                {
                  title: "Expert Insights",
                  description: "AI-generated summaries and explanations for better understanding of legal concepts"
                }
              ].map((feature, index) => (
                <div key={index} className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                  <BlurText
                    text={feature.title}
                    delay={100}
                    animateBy="words"
                    direction="top"
                    className="text-xl font-semibold text-white mb-4"
                  />
                  <ScrollReveal
                    baseOpacity={0.2}
                    enableBlur={true}
                    baseRotation={1}
                    blurStrength={4}
                    textClassName="text-white/70 text-sm leading-relaxed"
                  >
                    {feature.description}
                  </ScrollReveal>
                </div>
              ))}
            </div>
          </div>

          {/* Call to Action */}
          <div className="text-center px-4">
            <ScrollReveal
              baseOpacity={0.1}
              enableBlur={true}
              baseRotation={0}
              blurStrength={6}
              containerClassName="mb-8"
              textClassName="text-white text-center"
            >
              Ready to transform your legal research experience?
            </ScrollReveal>
            
            <div className="flex flex-wrap justify-center gap-4">
              <BlurText
                text="Start Exploring"
                delay={100}
                animateBy="words"
                direction="top"
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold transition-colors cursor-pointer"
              />
              <BlurText
                text="Learn More"
                delay={200}
                animateBy="words"
                direction="top"
                className="bg-white/10 hover:bg-white/20 text-white px-8 py-4 rounded-lg font-semibold border border-white/20 transition-colors cursor-pointer"
              />
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
