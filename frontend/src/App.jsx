import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './layouts/Layout';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import StudentDashboard from './pages/StudentDashboard';
import FacultyDashboard from './pages/FacultyDashboard';
import AdminDashboard from './pages/AdminDashboard';
import ComparePage from './pages/ComparePage';
import ResultsPage from './pages/ResultsPage';
import ReportHistory from './pages/ReportHistory';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<LandingPage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />
            
            <Route
              path="student-dashboard"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <StudentDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="faculty-dashboard"
              element={
                <ProtectedRoute allowedRoles={['faculty', 'admin']}>
                  <FacultyDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="admin-dashboard"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="compare"
              element={
                <ProtectedRoute allowedRoles={['student', 'faculty', 'admin']}>
                  <ComparePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="results/:comparisonId"
              element={
                <ProtectedRoute allowedRoles={['student', 'faculty', 'admin']}>
                  <ResultsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="history"
              element={
                <ProtectedRoute allowedRoles={['student', 'faculty', 'admin']}>
                  <ReportHistory />
                </ProtectedRoute>
              }
            />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
