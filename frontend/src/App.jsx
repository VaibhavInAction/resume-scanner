import React, { useState } from 'react';
import axios from 'axios';
import UploadResume from './components/UploadResume';
import JDInput from './components/JDInput';
import ScoreDisplay from './components/ScoreDisplay';
import SuggestionsList from './components/SuggestionsList';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [useLLM, setUseLLM] = useState(false);
  const [llmProvider, setLlmProvider] = useState('openrouter');

  const handleSubmit = async () => {
    // Validation
    if (!resumeFile) {
      setError('Please upload a resume file');
      return;
    }

    if (!jobDescription || jobDescription.length < 50) {
      setError('Please enter a job description (at least 50 characters)');
      return;
    }

    setError(null);
    setLoading(true);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('resume', resumeFile);
      formData.append('job_description', jobDescription);

      let endpoint = `${API_BASE_URL}/match`;
      
      if (useLLM) {
        endpoint = `${API_BASE_URL}/match-llm`;
        formData.append('provider', llmProvider);
      }

      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(
        err.response?.data?.detail || 
        'An error occurred while processing your request. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setJobDescription('');
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🤖 AI Resume Screener
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                Match resumes with job descriptions using AI-powered analysis
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                ● Online
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!results ? (
          /* Input Form */
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left Column - Resume Upload */}
            <div className="fade-in">
              <UploadResume 
                resumeFile={resumeFile}
                setResumeFile={setResumeFile}
              />
            </div>

            {/* Right Column - Job Description */}
            <div className="fade-in">
              <JDInput 
                jobDescription={jobDescription}
                setJobDescription={setJobDescription}
              />
            </div>

            {/* Full Width - Options and Submit */}
            <div className="lg:col-span-2 fade-in">
              <div className="bg-white rounded-lg shadow-md p-6">
                {/* LLM Options */}
                <div className="mb-6">
                  <div className="flex items-center mb-4">
                    <input
                      type="checkbox"
                      id="useLLM"
                      checked={useLLM}
                      onChange={(e) => setUseLLM(e.target.checked)}
                      className="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
                    />
                    <label htmlFor="useLLM" className="ml-2 text-sm font-medium text-gray-700">
                      🚀 Enable LLM-Enhanced Analysis (Optional)
                    </label>
                  </div>

                  {useLLM && (
                    <div className="ml-6 space-y-2">
                      <label className="text-sm text-gray-600">Select LLM Provider:</label>
                      <div className="flex space-x-4">
                        <label className="flex items-center">
                          <input
                            type="radio"
                            value="openrouter"
                            checked={llmProvider === 'openrouter'}
                            onChange={(e) => setLlmProvider(e.target.value)}
                            className="h-4 w-4 text-primary focus:ring-primary"
                          />
                          <span className="ml-2 text-sm text-gray-700">OpenRouter</span>
                        </label>
                        <label className="flex items-center">
                          <input
                            type="radio"
                            value="gemini"
                            checked={llmProvider === 'gemini'}
                            onChange={(e) => setLlmProvider(e.target.value)}
                            className="h-4 w-4 text-primary focus:ring-primary"
                          />
                          <span className="ml-2 text-sm text-gray-700">Gemini</span>
                        </label>
                      </div>
                    </div>
                  )}
                </div>

                {/* Error Message */}
                {error && (
                  <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm text-red-800">
                      ⚠️ {error}
                    </p>
                  </div>
                )}

                {/* Submit Button */}
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all duration-200 ${
                    loading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 transform hover:scale-[1.02] shadow-lg'
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                          fill="none"
                        />
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                      Analyzing... This may take a moment
                    </span>
                  ) : (
                    '🎯 Analyze Match'
                  )}
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* Results Display */
          <div className="space-y-6 fade-in">
            {/* Score Display */}
            <ScoreDisplay results={results} />

            {/* Suggestions */}
            <SuggestionsList suggestions={results.suggestions} />

            {/* Detailed Breakdown */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                📊 Detailed Breakdown
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Matched Skills */}
                <div>
                  <h4 className="font-semibold text-green-700 mb-2">
                    ✅ Matched Skills ({results.matched_skills?.length || 0})
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {results.matched_skills?.slice(0, 15).map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Missing Skills */}
                <div>
                  <h4 className="font-semibold text-red-700 mb-2">
                    ❌ Missing Skills ({results.missing_skills?.length || 0})
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {results.missing_skills?.slice(0, 15).map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* LLM Insights */}
              {results.llm_analysis && !results.llm_analysis.error && (
                <div className="mt-6 p-4 bg-purple-50 border border-purple-200 rounded-lg">
                  <h4 className="font-semibold text-purple-900 mb-2">
                    🤖 AI Insights ({results.llm_analysis.provider})
                  </h4>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {results.llm_analysis.llm_insights}
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex justify-center space-x-4">
              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition-colors"
              >
                🔄 Analyze Another Resume
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 text-center text-gray-600 text-sm">
        <p>Built with React, FastAPI, and AI 🚀</p>
      </footer>
    </div>
  );
}

export default App;
