'use client'

import React, { useState, useRef, useEffect } from 'react'
import { gsap } from 'gsap'
import { Scale, Menu, X, Search, BookOpen, BarChart3, Info } from 'lucide-react'

interface NavLink {
  label: string
  ariaLabel: string
  href?: string
}

interface NavItem {
  label: string
  bgColor: string
  textColor: string
  links: NavLink[]
  icon?: React.ReactNode
}

interface CardNavProps {
  logo?: string
  logoAlt?: string
  items: NavItem[]
  baseColor?: string
  menuColor?: string
  buttonBgColor?: string
  buttonTextColor?: string
  ease?: string
}

const CardNav: React.FC<CardNavProps> = ({
  logo,
  logoAlt = "Logo",
  items,
  baseColor = "#fff",
  menuColor = "#000",
  buttonBgColor = "#111",
  buttonTextColor = "#fff",
  ease = "power3.out"
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [activeItem, setActiveItem] = useState<number | null>(null)
  const menuRef = useRef<HTMLDivElement>(null)
  const overlayRef = useRef<HTMLDivElement>(null)
  const cardRefs = useRef<(HTMLDivElement | null)[]>([])

  useEffect(() => {
    if (isMenuOpen) {
      // Animate menu opening
      gsap.set(menuRef.current, { display: 'flex' })
      gsap.fromTo(overlayRef.current, 
        { opacity: 0 },
        { opacity: 1, duration: 0.3, ease }
      )
      
      // Stagger animate cards
      gsap.fromTo(cardRefs.current,
        { y: 50, opacity: 0 },
        { 
          y: 0, 
          opacity: 1, 
          duration: 0.4, 
          stagger: 0.1, 
          ease,
          delay: 0.1
        }
      )
    } else {
      // Animate menu closing
      gsap.to(overlayRef.current, {
        opacity: 0,
        duration: 0.3,
        ease,
        onComplete: () => {
          gsap.set(menuRef.current, { display: 'none' })
        }
      })
    }
  }, [isMenuOpen, ease])

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
    setActiveItem(null)
  }

  const handleItemHover = (index: number) => {
    setActiveItem(index)
  }

  return (
    <>
      {/* Navigation Bar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              {logo ? (
                <img src={logo} alt={logoAlt} className="h-8 w-auto" />
              ) : (
                <Scale className="h-8 w-8 text-blue-600" />
              )}
              <span className="text-xl font-bold text-gray-900">Legal RAG</span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#search" className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors">
                <Search className="h-4 w-4" />
                <span>Search</span>
              </a>
              <a href="#documents" className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors">
                <BookOpen className="h-4 w-4" />
                <span>Documents</span>
              </a>
              <a href="#analytics" className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors">
                <BarChart3 className="h-4 w-4" />
                <span>Analytics</span>
              </a>
              <a href="#about" className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors">
                <Info className="h-4 w-4" />
                <span>About</span>
              </a>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={toggleMenu}
              className="md:hidden p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-100 transition-colors"
              style={{ 
                backgroundColor: isMenuOpen ? buttonBgColor : 'transparent',
                color: isMenuOpen ? buttonTextColor : menuColor 
              }}
              aria-label="Toggle menu"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </nav>

      {/* Full Screen Menu Overlay */}
      <div
        ref={menuRef}
        className="fixed inset-0 z-40 hidden"
        style={{ display: 'none' }}
      >
        <div
          ref={overlayRef}
          className="absolute inset-0 bg-black/50 backdrop-blur-sm"
          onClick={toggleMenu}
        />
        
        <div className="relative z-50 flex items-center justify-center min-h-screen p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl w-full">
            {items.map((item, index) => (
              <div
                key={item.label}
                ref={(el) => { cardRefs.current[index] = el }}
                className="relative group cursor-pointer"
                onMouseEnter={() => handleItemHover(index)}
                onMouseLeave={() => setActiveItem(null)}
              >
                <div
                  className="rounded-2xl p-8 transition-all duration-300 transform group-hover:scale-105 group-hover:shadow-2xl"
                  style={{ 
                    backgroundColor: item.bgColor,
                    color: item.textColor
                  }}
                >
                  {/* Card Header */}
                  <div className="flex items-center space-x-3 mb-6">
                    {item.icon}
                    <h3 className="text-2xl font-bold">{item.label}</h3>
                  </div>

                  {/* Card Links */}
                  <div className="space-y-3">
                    {item.links.map((link) => (
                      <a
                        key={link.label}
                        href={link.href || '#'}
                        aria-label={link.ariaLabel}
                        className="block text-lg opacity-80 hover:opacity-100 transition-opacity duration-200 hover:translate-x-2 transform transition-transform"
                        onClick={toggleMenu}
                      >
                        {link.label}
                      </a>
                    ))}
                  </div>

                  {/* Hover Effect */}
                  <div 
                    className={`absolute inset-0 rounded-2xl transition-opacity duration-300 ${
                      activeItem === index ? 'opacity-10' : 'opacity-0'
                    }`}
                    style={{ backgroundColor: baseColor }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

export default CardNav
