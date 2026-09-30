import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Home, 
  FileText, 
  BarChart3, 
  Users, 
  Settings, 
  LogOut,
  Shield,
  BookOpen
} from 'lucide-react';

const Layout = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-2">
                <Shield className="h-8 w-8 text-primary-600" />
                <span className="text-xl font-bold text-gray-900">
                  Semantic Plagiarism Detector
                </span>
              </Link>
            </div>

            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/compare"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/compare')
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <FileText className="h-4 w-4 inline mr-1" />
                    Compare
                  </Link>
                  
                  {user?.role === 'student' && (
                    <Link
                      to="/student-dashboard"
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        isActive('/student-dashboard')
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <BarChart3 className="h-4 w-4 inline mr-1" />
                      Dashboard
                    </Link>
                  )}
                  
                  {user?.role === 'faculty' && (
                    <Link
                      to="/faculty-dashboard"
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        isActive('/faculty-dashboard')
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <BarChart3 className="h-4 w-4 inline mr-1" />
                      Dashboard
                    </Link>
                  )}
                  
                  {user?.role === 'admin' && (
                    <Link
                      to="/admin-dashboard"
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        isActive('/admin-dashboard')
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <Settings className="h-4 w-4 inline mr-1" />
                      Admin
                    </Link>
                  )}
                  
                  <Link
                    to="/history"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/history')
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <BookOpen className="h-4 w-4 inline mr-1" />
                    History
                  </Link>
                  
                  <button
                    onClick={logout}
                    className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100"
                  >
                    <LogOut className="h-4 w-4 inline mr-1" />
                    Logout
                  </button>
                  
                  <div className="flex items-center space-x-2 ml-4 pl-4 border-l border-gray-200">
                    <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center text-white font-medium">
                      {user?.full_name?.charAt(0).toUpperCase()}
                    </div>
                    <span className="text-sm text-gray-700">{user?.full_name}</span>
                  </div>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="px-4 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="px-4 py-2 rounded-md text-sm font-medium bg-primary-600 text-white hover:bg-primary-700"
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            © 2024 Semantic Plagiarism Detector. Academic project for demonstration purposes.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
