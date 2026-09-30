import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { comparisonsAPI } from '../services/api';
import { 
  BookOpen, 
  Trash2, 
  Search,
  Filter,
  Loader2,
  AlertCircle
} from 'lucide-react';

const ReportHistory = () => {
  const navigate = useNavigate();
  const [comparisons, setComparisons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterScore, setFilterScore] = useState('all');

  useEffect(() => {
    fetchComparisons();
  }, []);

  const fetchComparisons = async () => {
    try {
      const response = await comparisonsAPI.getAll();
      setComparisons(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch comparison history');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this comparison?')) {
      return;
    }

    try {
      await comparisonsAPI.delete(id);
      setComparisons(comparisons.filter(c => c.id !== id));
    } catch (err) {
      console.error('Failed to delete comparison:', err);
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

  const filteredComparisons = comparisons.filter(comparison => {
    const matchesSearch = comparison.id.toString().includes(searchTerm);
    const matchesFilter = filterScore === 'all' || 
      (filterScore === 'high' && comparison.overall_similarity >= 0.65) ||
      (filterScore === 'moderate' && comparison.overall_similarity >= 0.45 && comparison.overall_similarity < 0.65) ||
      (filterScore === 'low' && comparison.overall_similarity < 0.45);
    return matchesSearch && matchesFilter;
  });

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
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Report History</h1>
        <p className="text-gray-600">View and manage your plagiarism detection reports</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start">
          <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by comparison ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
          <div className="flex items-center">
            <Filter className="h-5 w-5 text-gray-400 mr-2" />
            <select
              value={filterScore}
              onChange={(e) => setFilterScore(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Scores</option>
              <option value="high">High Similarity (65%+)</option>
              <option value="moderate">Moderate Similarity (45-65%)</option>
              <option value="low">Low Similarity (&lt;45%)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Comparison List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        {filteredComparisons.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-4 px-6 text-sm font-medium text-gray-600">ID</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-gray-600">Date</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-gray-600">Similarity</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-gray-600">Processing Time</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-gray-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredComparisons.map((comparison) => (
                  <tr key={comparison.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-6">
                      <span className="font-medium text-gray-900">#{comparison.id}</span>
                    </td>
                    <td className="py-4 px-6 text-sm text-gray-600">
                      {new Date(comparison.created_at).toLocaleString()}
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getSimilarityColor(comparison.overall_similarity)}`}>
                          {getSimilarityLabel(comparison.overall_similarity)}
                        </span>
                        <span className="ml-2 font-bold text-gray-900">
                          {(comparison.overall_similarity * 100).toFixed(1)}%
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-6 text-sm text-gray-600">
                      {comparison.processing_time?.toFixed(2)}s
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => navigate(`/results/${comparison.id}`)}
                          className="px-3 py-1 text-sm text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded transition-colors"
                        >
                          View
                        </button>
                        <button
                          onClick={() => handleDelete(comparison.id)}
                          className="px-3 py-1 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded transition-colors"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            <BookOpen className="h-16 w-16 mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-medium mb-2">No comparisons found</p>
            <p className="text-sm mb-4">
              {searchTerm || filterScore !== 'all' 
                ? 'Try adjusting your filters or search terms'
                : 'Start by comparing your first document'}
            </p>
            {!searchTerm && filterScore === 'all' && (
              <button
                onClick={() => navigate('/compare')}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Start Comparison
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportHistory;
