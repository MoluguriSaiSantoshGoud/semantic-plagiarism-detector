import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { comparisonsAPI } from '../services/api';
import { FileText, Upload, X, AlertCircle, Loader2, FileUp, File } from 'lucide-react';

const ComparePage = () => {
  const [referenceText, setReferenceText] = useState('');
  const [submittedText, setSubmittedText] = useState('');
  const [referenceFilename, setReferenceFilename] = useState('reference.txt');
  const [submittedFilename, setSubmittedFilename] = useState('submitted.txt');
  const [referenceFile, setReferenceFile] = useState(null);
  const [submittedFile, setSubmittedFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileUpload = async (file, type) => {
    if (!file) return;

    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.pdf') && !file.name.endsWith('.docx') && !file.name.endsWith('.txt')) {
      setError('Invalid file type. Please upload PDF, DOCX, or TXT files.');
      return;
    }

    if (type === 'reference') {
      setReferenceFile(file);
      setReferenceFilename(file.name);
      const text = await extractTextFromFile(file);
      setReferenceText(text);
    } else {
      setSubmittedFile(file);
      setSubmittedFilename(file.name);
      const text = await extractTextFromFile(file);
      setSubmittedText(text);
    }
  };

  const extractTextFromFile = async (file) => {
    if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
      return await file.text();
    }
    // For PDF and DOCX, we'll need to send to backend for extraction
    // For now, return a placeholder
    return `[File content will be extracted from ${file.name} on the server]`;
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e, type) => {
    e.preventDefault();
    e.stopPropagation();
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload(file, type);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!referenceText.trim() || !submittedText.trim()) {
      setError('Both reference and submitted text are required');
      return;
    }

    setLoading(true);

    try {
      const response = await comparisonsAPI.create({
        reference_text: referenceText,
        submitted_text: submittedText,
        reference_filename: referenceFilename,
        submitted_filename: submittedFilename,
      });

      navigate(`/results/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Comparison failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setReferenceText('');
    setSubmittedText('');
    setReferenceFile(null);
    setSubmittedFile(null);
    setReferenceFilename('reference.txt');
    setSubmittedFilename('submitted.txt');
    setError('');
  };

  const removeFile = (type) => {
    if (type === 'reference') {
      setReferenceFile(null);
      setReferenceText('');
      setReferenceFilename('reference.txt');
    } else {
      setSubmittedFile(null);
      setSubmittedText('');
      setSubmittedFilename('submitted.txt');
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Compare Documents</h1>
        <p className="text-gray-600">
          Upload files (PDF, DOCX, TXT) or paste text to detect semantic similarity
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start">
          <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Reference Document */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <FileText className="h-5 w-5 text-primary-600 mr-2" />
                <h2 className="text-lg font-semibold text-gray-900">Reference Document</h2>
              </div>
              {referenceFile && (
                <button
                  type="button"
                  onClick={() => removeFile('reference')}
                  className="text-red-500 hover:text-red-600"
                >
                  <X className="h-5 w-5" />
                </button>
              )}
            </div>

            {/* File Upload Area */}
            <div
              className={`mb-4 border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
                referenceFile ? 'border-primary-300 bg-primary-50' : 'border-gray-300 hover:border-primary-400'
              }`}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, 'reference')}
            >
              {referenceFile ? (
                <div className="flex items-center justify-center">
                  <File className="h-8 w-8 text-primary-600 mr-2" />
                  <span className="text-sm font-medium text-gray-700">{referenceFile.name}</span>
                </div>
              ) : (
                <>
                  <FileUp className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-600 mb-2">
                    Drag & drop a file here, or
                  </p>
                  <label className="inline-block px-4 py-2 bg-primary-600 text-white rounded-lg cursor-pointer hover:bg-primary-700 transition-colors">
                    Browse Files
                    <input
                      type="file"
                      className="hidden"
                      accept=".pdf,.docx,.txt"
                      onChange={(e) => handleFileUpload(e.target.files[0], 'reference')}
                    />
                  </label>
                  <p className="text-xs text-gray-500 mt-2">
                    PDF, DOCX, or TXT (max 10MB)
                  </p>
                </>
              )}
            </div>

            {/* Text Input Area */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Or paste text directly
              </label>
              <textarea
                value={referenceText}
                onChange={(e) => setReferenceText(e.target.value)}
                rows={8}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
                placeholder="Paste the reference text here..."
              />
              <p className="text-xs text-gray-500 mt-1">
                {referenceText.split(/\s+/).filter(word => word).length} words
              </p>
            </div>
          </div>

          {/* Submitted Document */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <FileText className="h-5 w-5 text-primary-600 mr-2" />
                <h2 className="text-lg font-semibold text-gray-900">Submitted Document</h2>
              </div>
              {submittedFile && (
                <button
                  type="button"
                  onClick={() => removeFile('submitted')}
                  className="text-red-500 hover:text-red-600"
                >
                  <X className="h-5 w-5" />
                </button>
              )}
            </div>

            {/* File Upload Area */}
            <div
              className={`mb-4 border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
                submittedFile ? 'border-primary-300 bg-primary-50' : 'border-gray-300 hover:border-primary-400'
              }`}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, 'submitted')}
            >
              {submittedFile ? (
                <div className="flex items-center justify-center">
                  <File className="h-8 w-8 text-primary-600 mr-2" />
                  <span className="text-sm font-medium text-gray-700">{submittedFile.name}</span>
                </div>
              ) : (
                <>
                  <FileUp className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-600 mb-2">
                    Drag & drop a file here, or
                  </p>
                  <label className="inline-block px-4 py-2 bg-primary-600 text-white rounded-lg cursor-pointer hover:bg-primary-700 transition-colors">
                    Browse Files
                    <input
                      type="file"
                      className="hidden"
                      accept=".pdf,.docx,.txt"
                      onChange={(e) => handleFileUpload(e.target.files[0], 'submitted')}
                    />
                  </label>
                  <p className="text-xs text-gray-500 mt-2">
                    PDF, DOCX, or TXT (max 10MB)
                  </p>
                </>
              )}
            </div>

            {/* Text Input Area */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Or paste text directly
              </label>
              <textarea
                value={submittedText}
                onChange={(e) => setSubmittedText(e.target.value)}
                rows={8}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
                placeholder="Paste the submitted text here..."
              />
              <p className="text-xs text-gray-500 mt-1">
                {submittedText.split(/\s+/).filter(word => word).length} words
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between items-center">
          <button
            type="button"
            onClick={clearAll}
            className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Clear All
          </button>

          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Upload className="h-5 w-5 mr-2" />
                Check Plagiarism
              </>
            )}
          </button>
        </div>
      </form>

      {/* Info Box */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
          <div className="text-sm text-blue-800">
            <p className="font-semibold mb-1">How it works</p>
            <p>
              The system uses semantic analysis to detect meaning-based similarities, not just word-for-word matches. 
              It can identify paraphrasing, conceptual similarities, and direct copying. Results include detailed 
              explanations for each flagged section.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComparePage;
