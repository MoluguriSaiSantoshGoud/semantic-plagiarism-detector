# Frontend - Semantic Plagiarism Detection

React frontend for semantic plagiarism detection system.

## Setup

1. Install dependencies:
```bash
npm install
```

## Running

Development mode:
```bash
npm run dev
```

Production build:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Project Structure

```
src/
├── components/      # Reusable components
│   └── ProtectedRoute.jsx
├── pages/          # Page components
│   ├── LandingPage.jsx
│   ├── LoginPage.jsx
│   ├── RegisterPage.jsx
│   ├── StudentDashboard.jsx
│   ├── FacultyDashboard.jsx
│   ├── AdminDashboard.jsx
│   ├── ComparePage.jsx
│   ├── ResultsPage.jsx
│   └── ReportHistory.jsx
├── layouts/        # Layout components
│   └── Layout.jsx
├── services/       # API services
│   └── api.js
├── context/        # React context
│   └── AuthContext.jsx
├── App.jsx         # Main app component
└── main.jsx        # Entry point
```

## Features

- **Authentication** - Login, registration, logout with JWT
- **Role-based Access** - Student, faculty, and admin dashboards
- **Document Comparison** - Text input for plagiarism detection
- **Results Display** - Detailed similarity analysis with explanations
- **Report Generation** - PDF download functionality
- **History Management** - View and manage past comparisons

## Styling

Uses Tailwind CSS for styling with a clean, professional white and blue theme.

## API Integration

All API calls are handled through the `api.js` service layer with automatic token injection and error handling.
