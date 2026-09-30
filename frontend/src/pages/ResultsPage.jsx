import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { comparisonsAPI, reportsAPI } from '../services/api';
import { 
  ArrowLeft, 
  Download, 
  AlertCircle, 
  Loader2,
  FileText,
  BarChart3,
  CheckCircle,
  XCircle
} from 'lucide-react';

const ResultsPage = () => {
  const { comparisonId } = useParams();
  const navigate = useNavigate();
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [downloadingReport, setDownloadingReport] = useState(false);

  useEffect(() => {
    fetchComparison();
  }, [comparisonId]);

  const fetchComparison = async () => {
    try {
      const response = await comparisonsAPI.getById(comparisonId);
      setComparison(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load comparison results');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    setDownloadingReport(true);
    try {
      // First generate the report
      await reportsAPI.generate(comparisonId);
      
      // Then download it
      const response = await reportsAPI.download(comparisonId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `plagiarism_report_${comparisonId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Failed to download report:', err);
    } finally {
      setDownloadingReport(false);
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

  const getClassificationIcon = (classification) => {
    switch (classification) {
      case 'Exact copy':
      case 'Near-exact copy':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'Likely paraphrase':
        return <AlertCircle className="h-5 w-5 text-orange-600" />;
      case 'Conceptually similar':
        return <AlertCircle className="h-5 w-5 text-yellow-600" />;
      default:
        return <CheckCircle className="h-5 w-5 text-green-600" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
        <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
        <p className="text-sm text-red-800">{error}</p>
      </div>
    );
  }

  if (!comparison) {
    return null;
  }

  const overallScore = comparison.overall_similarity * 100;
  const stats = comparison.statistics || {};

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/compare')}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="h-5 w-5 mr-2" />
          Back to Compare
        </button>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Plagiarism Detection Results</h1>
        <p className="text-gray-600">
          Comparison between {comparison.reference_document?.filename} and {comparison.submitted_document?.filename}
        </p>
      </div>

      {/* Overall Score Card */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Overall Similarity</h2>
            <p className="text-gray-600">Based on semantic, lexical, and n-gram analysis</p>
          </div>
          <div className="text-right">
            <div className={`text-6xl font-bold ${getSimilarityColor(comparison.overall_similarity).split(' ')[0]}`}>
              {overallScore.toFixed(1)}%
            </div>
            <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium mt-2 ${getSimilarityColor(comparison.overall_similarity)}`}>
              {getSimilarityLabel(comparison.overall_similarity)} Similarity
            </div>
          </div>
        </div>
      </div>

      {/* Statistics Grid */}
      <div className="grid md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Total Chunks</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_submitted_chunks || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <BarChart3 className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Matching Chunks</p>
              <p className="text-2xl font-bold text-gray-900">{stats.matching_chunk_count || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-orange-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">High Risk</p>
              <p className="text-2xl font-bold text-gray-900">
                {(stats.very_high_similarity_chunk_count || 0) + (stats.high_similarity_chunk_count || 0)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Processing Time</p>
              <p className="text-2xl font-bold text-gray-900">{comparison.processing_time?.toFixed(2)}s</p>
            </div>
          </div>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Score Breakdown</h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Semantic Score</p>
            <p className="text-xl font-bold text-gray-900">
              {(comparison.weighted_similarity * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-gray-500">Meaning-based similarity</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Lexical Score</p>
            <p className="text-xl font-bold text-gray-900">
              {(comparison.overall_similarity * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-gray-500">Word-based similarity</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">N-gram Score</p>
            <p className="text-xl font-bold text-gray-900">
              {(comparison.overall_similarity * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-gray-500">Phrase-based similarity</p>
          </div>
        </div>
      </div>

      {/* Matching Sections */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Matching Sections</h3>
          <button
            onClick={handleDownloadReport}
            disabled={downloadingReport}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 flex items-center text-sm"
          >
            {downloadingReport ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Download className="h-4 w-4 mr-2" />
                Download Report
              </>
            )}
          </button>
        </div>

        {comparison.matches && comparison.matches.length > 0 ? (
          <div className="space-y-4">
            {comparison.matches.map((match, index) => (
              <div key={match.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center">
                    {getClassificationIcon(match.classification)}
                    <span className="ml-2 font-medium text-gray-900">Match #{index + 1}</span>
                    <span className={`ml-3 px-2 py-1 rounded text-xs font-medium ${getSimilarityColor(match.combined_score)}`}>
                      {(match.combined_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <span className="text-sm text-gray-600">{match.classification}</span>
                </div>

                <div className="grid md:grid-cols-2 gap-4 mb-3">
                  <div>
                    <p className="text-xs font-medium text-gray-500 mb-1">REFERENCE</p>
                    <p className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                      {match.reference_text?.substring(0, 200)}
                      {match.reference_text?.length > 200 && '...'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs font-medium text-gray-500 mb-1">SUBMITTED</p>
                    <p className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                      {match.submitted_text?.substring(0, 200)}
                      {match.submitted_text?.length > 200 && '...'}
                    </p>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded p-3">
                  <p className="text-xs text-blue-800">{match.explanation}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <CheckCircle className="h-12 w-12 mx-auto mb-3 text-green-600" />
            <p>No significant matches found</p>
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5 mr-3 flex-shrink-0" />
          <div className="text-sm text-yellow-800">
            <p className="font-semibold mb-1">Important Disclaimer</p>
            <p>
              This report provides similarity indicators based on computational text analysis. 
              It is not a definitive determination of academic misconduct. Final interpretation 
              should be performed by qualified human reviewers considering context, citations, 
              and assignment requirements.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
