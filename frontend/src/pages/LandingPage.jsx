import { Link } from 'react-router-dom';
import { Shield, FileText, Brain, BarChart3, CheckCircle, ArrowRight } from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="bg-primary-600 p-4 rounded-2xl">
                <Shield className="h-16 w-16 text-white" />
              </div>
            </div>
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Semantic Plagiarism Detection
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Detect plagiarism based on meaning, not just matching words. Identify exact copying, 
              paraphrasing, and semantically similar content between documents using advanced NLP.
            </p>
            <div className="flex justify-center space-x-4">
              <Link
                to="/register"
                className="px-8 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center"
              >
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/login"
                className="px-8 py-3 bg-white text-primary-600 border border-primary-600 rounded-lg font-medium hover:bg-gray-50 transition-colors"
              >
                Login
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Powerful Features
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gray-50 rounded-xl p-6">
              <div className="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <Brain className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Semantic Analysis
              </h3>
              <p className="text-gray-600">
                Uses advanced sentence transformers to understand meaning and detect paraphrasing, 
                not just word-for-word copying.
              </p>
            </div>

            <div className="bg-gray-50 rounded-xl p-6">
              <div className="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Multiple Formats
              </h3>
              <p className="text-gray-600">
                Support for PDF, DOCX, and TXT files with intelligent text extraction and 
                paragraph-level analysis.
              </p>
            </div>

            <div className="bg-gray-50 rounded-xl p-6">
              <div className="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Detailed Reports
              </h3>
              <p className="text-gray-600">
                Comprehensive similarity reports with score breakdowns, match classifications, 
                and downloadable PDF reports.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-primary-600 text-white w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-4 font-bold">
                1
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Upload Documents</h3>
              <p className="text-gray-600 text-sm">
                Upload reference and submitted documents or paste text directly
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-600 text-white w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-4 font-bold">
                2
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Text Processing</h3>
              <p className="text-gray-600 text-sm">
                Documents are split into chunks and analyzed with NLP
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-600 text-white w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-4 font-bold">
                3
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Similarity Analysis</h3>
              <p className="text-gray-600 text-sm">
                Hybrid engine compares semantic, lexical, and n-gram similarities
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-600 text-white w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-4 font-bold">
                4
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">View Results</h3>
              <p className="text-gray-600 text-sm">
                Get detailed reports with match classifications and explanations
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-primary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Detect Plagiarism?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Start using our semantic plagiarism detection system today. Perfect for academic 
            institutions and content verification.
          </p>
          <Link
            to="/register"
            className="px-8 py-3 bg-white text-primary-600 rounded-lg font-medium hover:bg-gray-100 transition-colors inline-flex items-center"
          >
            Create Account
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="py-8 bg-gray-50 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-start">
              <CheckCircle className="h-5 w-5 text-yellow-600 mt-0.5 mr-3" />
              <div>
                <h4 className="font-semibold text-yellow-800 mb-1">Important Note</h4>
                <p className="text-sm text-yellow-700">
                  This system provides similarity indicators based on computational text analysis. 
                  It is not a definitive determination of academic misconduct. Final interpretation 
                  should be performed by qualified human reviewers considering context, citations, 
                  and assignment requirements.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
