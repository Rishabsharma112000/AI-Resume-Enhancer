# Frontend Setup Instructions

## Prerequisites

- Node.js 16+ and npm/yarn
- Backend API running on `http://localhost:8000`

## Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Environment setup:**
Create a `.env.local` file:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

3. **Run development server:**
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable React components
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── store/            # Zustand state management
│   ├── types/            # TypeScript types
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utility functions
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── index.html            # HTML entry point
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies
```

## Key Features

### Components
- **Layout** - Main layout with sidebar and navbar
- **ResumeUpload** - Drag-and-drop resume upload
- **ResumeList** - Browse and manage resumes
- **AnalysisResults** - Display analysis metrics
- **JobDescriptionForm** - Create/upload job descriptions

### Pages
- **LoginPage** - User authentication
- **RegisterPage** - New user registration
- **DashboardPage** - Main dashboard with resume management
- **ProfilePage** - User profile management
- **AnalysisPage** - Detailed analysis view

### State Management
- Uses Zustand for global auth state
- Local storage persistence
- Automatic token management

### API Integration
- Axios client with interceptors
- Automatic token injection
- Error handling and redirects
- Service layer for all API calls

## Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run type-check   # Check TypeScript types
```

## Styling

- **Tailwind CSS** - Utility-first CSS framework
- **Custom components** - Pre-built component library
- **Responsive design** - Mobile-first approach
- **Dark mode support** - Can be easily added

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

## Performance Optimizations

- Code splitting with Vite
- Lazy loading for routes
- Image optimization
- CSS tree-shaking
- Minification in production

## Troubleshooting

### API Connection Issues
```bash
# Check backend is running
curl http://localhost:8000/health

# Update VITE_API_URL in .env.local if needed
```

### Module Not Found
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
npm run type-check
```

## Development Tips

1. Use React DevTools browser extension for debugging
2. Check browser console for API errors
3. Use VS Code Vetur/Volar extension for TypeScript support
4. Hot reload is enabled automatically during development

## License

MIT License
