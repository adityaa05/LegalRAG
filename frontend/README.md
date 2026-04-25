# Legal RAG System - Frontend

A modern, AI-powered legal research assistant built with Next.js, React, and Tailwind CSS. This frontend interfaces with a comprehensive Legal RAG (Retrieval-Augmented Generation) backend that processes Indian legal documents.

## 🏛️ System Overview

This frontend provides an intuitive interface for:
- **AI-powered legal search** across 7 major Indian legal documents
- **Smart document browsing** with hierarchical navigation
- **RAG-powered responses** with source citations and legal metadata
- **Advanced filtering** by document type, offense category, and severity

## 📚 Available Legal Documents

- **Indian Penal Code (IPC)** - 615 sections
- **Criminal Procedure Code (CrPC)** - 22 sections  
- **Civil Procedure Code (CPC)** - 104 sections
- **Indian Constitution** - 295 articles
- **Indian Evidence Act** - 6 sections
- **Companies Act 2013** - 60 sections
- **Income Tax Act 1961** - 234 sections

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm/yarn/pnpm
- Legal RAG backend running (see `../legal-rag/` directory)

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## 🎨 Current Status

**✅ Completed:**
- Next.js project setup with TypeScript and Tailwind CSS
- Interactive wireframe component showing planned UI/UX
- Project structure and documentation

**🔄 In Progress:**
- Core component development
- API integration with backend
- Search interface implementation

**📋 Planned Features:**
- Smart search with autocomplete
- Document browser with section navigation
- RAG response display with citations
- Legal analytics dashboard
- Mobile-responsive design

## 🛠️ Tech Stack

- **Framework:** Next.js 15 with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **UI Components:** Radix UI primitives
- **State Management:** React Context + Local Storage

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # Reusable React components
│   │   ├── Wireframe.tsx   # Interactive wireframe (current)
│   │   ├── SearchInterface.tsx    # (planned)
│   │   ├── DocumentBrowser.tsx    # (planned)
│   │   ├── RAGResponse.tsx        # (planned)
│   │   └── Analytics.tsx          # (planned)
│   ├── lib/                # Utility functions
│   └── types/              # TypeScript type definitions
├── public/                 # Static assets
├── WIREFRAME.md           # Detailed wireframe documentation
└── README.md              # This file
```

## 🎯 Development Roadmap

### Phase 1: Core Interface (Current)
- [x] Project setup and wireframe
- [ ] Search interface component
- [ ] Basic document browser
- [ ] API integration setup

### Phase 2: RAG Integration
- [ ] Backend API connection
- [ ] Search results display
- [ ] AI response formatting
- [ ] Source citation system

### Phase 3: Advanced Features
- [ ] Legal analytics dashboard
- [ ] Advanced filtering system
- [ ] User preferences and history
- [ ] Export functionality

### Phase 4: Polish & Performance
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] Accessibility improvements
- [ ] Error handling

## 🔗 API Integration

The frontend will connect to the Legal RAG backend through these endpoints:

```typescript
// Planned API endpoints
POST /api/search          // RAG-powered search
GET  /api/documents       // Document metadata
GET  /api/sections/:id    // Individual section content
GET  /api/analytics       // Usage statistics
```

## 🎨 Design System

- **Colors:** Professional legal theme with blue/gray palette
- **Typography:** Clean, readable fonts optimized for legal text
- **Layout:** Responsive grid with sidebar navigation
- **Components:** Consistent design language across all interfaces

## 📱 Responsive Design

- **Desktop:** Full-featured interface with sidebar and multi-panel layout
- **Tablet:** Collapsible sidebar with stacked panels
- **Mobile:** Bottom navigation with full-screen panels

## 🔧 Development Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript checks

# Utilities
npm run clean        # Clean build artifacts
npm run analyze      # Bundle size analysis
```

## 📖 Documentation

- [Wireframe Documentation](./WIREFRAME.md) - Detailed UI/UX specifications
- [Component Guide](./docs/components.md) - Component documentation (planned)
- [API Integration](./docs/api.md) - Backend integration guide (planned)

## 🤝 Contributing

1. Follow the existing code style and conventions
2. Write TypeScript with proper type definitions
3. Use Tailwind CSS for styling
4. Test components thoroughly before committing
5. Update documentation for new features

## 🔮 Future Enhancements

- **Multi-language Support:** Hindi and regional languages
- **Voice Search:** Speech-to-text integration
- **Legal Case Integration:** Supreme Court and High Court cases
- **Collaborative Features:** Shared research and annotations
- **Mobile App:** React Native companion app
- **Offline Mode:** Cached content for offline access

## 📄 License

This project is part of the Legal RAG System for educational and research purposes.

---

**Current Status:** 🎨 Wireframe Complete - Ready for Component Development

Visit the wireframe at [http://localhost:3000](http://localhost:3000) to see the planned interface!
