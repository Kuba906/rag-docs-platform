# RAG Docs Platform - Frontend

React + TypeScript frontend for the RAG Docs Platform.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests
- **ESLint** - Code linting
- **Prettier** - Code formatting

## Prerequisites

- Node.js 18+ and npm (or yarn/pnpm)

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` to point to your backend API (default is `http://localhost:8000`):

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── services/       # API services
│   │   ├── api.ts      # Axios configuration
│   │   └── ragService.ts # RAG API methods
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── index.css       # Global styles + Tailwind
├── public/             # Static assets
├── index.html          # HTML template
├── vite.config.ts      # Vite configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── tsconfig.json       # TypeScript configuration
└── package.json        # Dependencies and scripts
```

## API Integration

The frontend connects to the backend API using the `RagService` class:

```typescript
import RagService from './services/ragService';

// Check health
const health = await RagService.checkHealth();

// Upload document
const result = await RagService.ingestDocument(file);

// Ask question
const answer = await RagService.askQuestion('What is this about?');
```

## Building for Production

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

## Code Style

This project uses ESLint and Prettier for consistent code style:

- Run `npm run lint` to check for issues
- Run `npm run lint:fix` to auto-fix issues
- Run `npm run format` to format code

## Next Steps

Implement the remaining components from the roadmap:
- Document upload component (#2)
- Search interface (#3)
- Answer display component (#4)
- Sources/citations list (#5)
- Document library sidebar (#6)
- Metrics dashboard (#7)
- Dark mode toggle (#8)
