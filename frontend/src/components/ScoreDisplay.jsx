import React from 'react';

function ScoreDisplay({ results }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent Match';
    if (score >= 60) return 'Good Match';
    if (score >= 40) return 'Fair Match';
    return 'Poor Match';
  };

  const ScoreBar = ({ label, score, color }) => (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="font-medium text-gray-700">{label}</span>
        <span className={`font-bold ${getScoreColor(score)}`}>
          {score.toFixed(1)}%
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className={`h-3 rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Overall Score */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Match Score
        </h2>
        <div className="relative inline-flex items-center justify-center">
          <svg className="w-40 h-40 transform -rotate-90">
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="currentColor"
              strokeWidth="12"
              fill="transparent"
              className="text-gray-200"
            />
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="currentColor"
              strokeWidth="12"
              fill="transparent"
              strokeDasharray={`${2 * Math.PI * 70}`}
              strokeDashoffset={`${2 * Math.PI * 70 * (1 - results.overall_score / 100)}`}
              className={getScoreColor(results.overall_score)}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-4xl font-bold ${getScoreColor(results.overall_score)}`}>
              {results.overall_score.toFixed(0)}%
            </span>
            <span className="text-sm text-gray-600 mt-1">
              {getScoreLabel(results.overall_score)}
            </span>
          </div>
        </div>
      </div>

      {/* Detailed Scores */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-gray-900 mb-3">
          Score Breakdown
        </h3>

        <ScoreBar
          label="Skills Match"
          score={results.keyword_match_score}
          color={getScoreBgColor(results.keyword_match_score)}
        />

        <ScoreBar
          label="Semantic Similarity"
          score={results.semantic_similarity_score}
          color={getScoreBgColor(results.semantic_similarity_score)}
        />

        <ScoreBar
          label="Experience Match"
          score={results.experience_score}
          color={getScoreBgColor(results.experience_score)}
        />

        <ScoreBar
          label="Education Match"
          score={results.education_score}
          color={getScoreBgColor(results.education_score)}
        />
      </div>

      {/* Quick Stats */}
      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-green-700">
            {results.matched_skills?.length || 0}
          </p>
          <p className="text-sm text-gray-600">Skills Matched</p>
        </div>
        <div className="bg-red-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-red-700">
            {results.missing_skills?.length || 0}
          </p>
          <p className="text-sm text-gray-600">Skills Missing</p>
        </div>
      </div>
    </div>
  );
}

export default ScoreDisplay;
