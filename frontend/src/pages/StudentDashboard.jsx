import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardAPI, comparisonsAPI } from '../services/api';
import { 
  BarChart3, 
  FileText, 
  AlertTriangle, 
  Clock,
  Plus,
  Loader2
} from 'lucide-react';

const StudentDashboard = () => {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await dashboardAPI.student();
      setDashboardData(response.data);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSimilarityColor = (score) => {
    if (score >= 0.80) return 'text-red-600 bg-red-100';
    if (score >= 0.65) return 'text-orange-600 bg-orange-100';
    if (score >= 0.45) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const getSimilarityLabel = (score) => {
    if (score >= 0.80) return 'Very High';
    if (score >= 0.65) return 'High';
    if (score >= 0.45) return 'Moderate';
    return 'Low';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Student Dashboard</h1>
        <p className="text-gray-600">Overview of your plagiarism detection results</p>
      </div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Total Comparisons</p>
              <p className="text-2xl font-bold text-gray-900">
                {dashboardData?.total_comparisons || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <BarChart3 className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Avg Similarity</p>
              <p className="text-2xl font-bold text-gray-900">
                {((dashboardData?.average_similarity || 0) * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-orange-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">High Risk Reports</p>
              <p className="text-2xl font-bold text-gray-900">
                {dashboardData?.high_risk_reports || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <button
            onClick={() => navigate('/compare')}
            className="w-full h-full flex items-center justify-center text-primary-600 hover:text-primary-700"
          >
            <Plus className="h-8 w-8 mr-2" />
            <span className="font-medium">New Comparison</span>
          </button>
        </div>
      </div>

      {/* Recent Comparisons */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Comparisons</h2>
        
        {dashboardData?.recent_comparisons && dashboardData.recent_comparisons.length > 0 ? (
          <div className="space-y-3">
            {dashboardData.recent_comparisons.map((comparison) => (
              <div
                key={comparison.id}
                onClick={() => navigate(`/results/${comparison.id}`)}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div className="flex items-center">
                  <Clock className="h-5 w-5 text-gray-400 mr-3" />
                  <div>
                    <p className="font-medium text-gray-900">Comparison #{comparison.id}</p>
                    <p className="text-sm text-gray-600">
                      {new Date(comparison.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSimilarityColor(comparison.overall_similarity)}`}>
                    {getSimilarityLabel(comparison.overall_similarity)}
                  </span>
                  <span className="ml-3 text-lg font-bold text-gray-900">
                    {(comparison.overall_similarity * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <FileText className="h-12 w-12 mx-auto mb-3 text-gray-400" />
            <p>No comparisons yest</p>
            <button
              onClick={() => navigate('/compare')}
              className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Start Your First Comparison
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentDashboard;
