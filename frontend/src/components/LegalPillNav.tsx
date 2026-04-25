'use client'

import React from 'react'

const LegalPillNav = () => {
  const navItems = [
    { label: 'Home', href: '/', ariaLabel: 'Go to homepage' },
    { label: 'Search', href: '#search', ariaLabel: 'Legal search' },
    { label: 'Documents', href: '#documents', ariaLabel: 'Browse legal documents' },
    { label: 'Analytics', href: '#analytics', ariaLabel: 'View analytics' },
    { label: 'About', href: '#about', ariaLabel: 'About KnowYourCrime' }
  ]

  return (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-[1000] w-full max-w-[95vw] px-2">
      <nav className="flex items-center justify-center bg-white/10 dark:bg-black/20 backdrop-blur-md rounded-full border border-white/20 dark:border-white/10 px-1 sm:px-2 py-2 shadow-lg">
        <ul className="flex items-center space-x-1 sm:space-x-2 overflow-x-auto scrollbar-hide">
          {navItems.map((item, index) => (
            <li key={item.href} className="flex-shrink-0">
              <a
                href={item.href}
                aria-label={item.ariaLabel}
                className="relative px-2 sm:px-4 md:px-6 py-2 sm:py-3 text-xs sm:text-sm md:text-base font-normal text-white dark:text-white hover:text-white transition-all duration-300 rounded-full hover:bg-red-600 dark:hover:bg-red-500 hover:shadow-md transform hover:scale-105 font-almarai whitespace-nowrap"
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  )
}

export default LegalPillNav
