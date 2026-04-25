'use client'

import React from 'react'
import CardNav from './CardNav'
import { Search, BookOpen, BarChart3, Info, Scale, Gavel, Shield, FileText } from 'lucide-react'

const LegalNavigation = () => {
  const items = [
    {
      label: "Search",
      bgColor: "#1e40af", // Blue theme for search
      textColor: "#fff",
      icon: <Search className="h-6 w-6" />,
      links: [
        { label: "AI Legal Search", ariaLabel: "AI-powered legal search", href: "#search" },
        { label: "Quick Search", ariaLabel: "Quick legal search", href: "#quick-search" },
        { label: "Advanced Filters", ariaLabel: "Advanced search filters", href: "#filters" },
        { label: "Search History", ariaLabel: "View search history", href: "#history" }
      ]
    },
    {
      label: "Documents", 
      bgColor: "#059669", // Green theme for documents
      textColor: "#fff",
      icon: <BookOpen className="h-6 w-6" />,
      links: [
        { label: "Indian Penal Code", ariaLabel: "Browse IPC sections", href: "#ipc" },
        { label: "Constitution", ariaLabel: "Browse Constitution articles", href: "#constitution" },
        { label: "Criminal Procedure", ariaLabel: "Browse CrPC sections", href: "#crpc" },
        { label: "Civil Procedure", ariaLabel: "Browse CPC sections", href: "#cpc" },
        { label: "Evidence Act", ariaLabel: "Browse Evidence Act", href: "#evidence" },
        { label: "Companies Act", ariaLabel: "Browse Companies Act", href: "#companies" },
        { label: "Income Tax Act", ariaLabel: "Browse Income Tax Act", href: "#income-tax" }
      ]
    },
    {
      label: "Analytics",
      bgColor: "#7c3aed", // Purple theme for analytics
      textColor: "#fff",
      icon: <BarChart3 className="h-6 w-6" />,
      links: [
        { label: "Legal Insights", ariaLabel: "View legal analytics", href: "#insights" },
        { label: "Usage Statistics", ariaLabel: "View usage statistics", href: "#stats" },
        { label: "Offense Trends", ariaLabel: "View offense trends", href: "#trends" },
        { label: "Document Coverage", ariaLabel: "View document coverage", href: "#coverage" }
      ]
    },
    {
      label: "Resources",
      bgColor: "#dc2626", // Red theme for resources
      textColor: "#fff",
      icon: <Scale className="h-6 w-6" />,
      links: [
        { label: "Legal Categories", ariaLabel: "Browse legal categories", href: "#categories" },
        { label: "Punishment Guide", ariaLabel: "Punishment severity guide", href: "#punishment" },
        { label: "Case References", ariaLabel: "Legal case references", href: "#cases" },
        { label: "Legal Glossary", ariaLabel: "Legal terms glossary", href: "#glossary" }
      ]
    },
    {
      label: "About",
      bgColor: "#374151", // Gray theme for about
      textColor: "#fff",
      icon: <Info className="h-6 w-6" />,
      links: [
        { label: "About Legal RAG", ariaLabel: "About the Legal RAG system", href: "#about" },
        { label: "How It Works", ariaLabel: "How the system works", href: "#how-it-works" },
        { label: "Data Sources", ariaLabel: "Legal data sources", href: "#sources" },
        { label: "API Documentation", ariaLabel: "API documentation", href: "#api-docs" },
        { label: "Contact Support", ariaLabel: "Contact support", href: "#support" }
      ]
    }
  ];

  return (
    <CardNav
      logoAlt="Legal RAG System Logo"
      items={items}
      baseColor="#f8fafc"
      menuColor="#374151"
      buttonBgColor="#1e40af"
      buttonTextColor="#fff"
      ease="power3.out"
    />
  );
};

export default LegalNavigation
