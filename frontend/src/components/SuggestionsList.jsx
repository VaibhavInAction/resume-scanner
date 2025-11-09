import React from 'react';

function SuggestionsList({ suggestions }) {
  if (!suggestions || suggestions.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
        <span className="text-2xl mr-2">💡</span>
        Improvement Suggestions
      </h3>

      <div className="space-y-3">
        {suggestions.map((suggestion, index) => (
          <div
            key={index}
            className="flex items-start p-4 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-primary text-white rounded-full text-sm font-bold mr-3 mt-0.5">
              {index + 1}
            </span>
            <p className="text-gray-800 text-sm leading-relaxed">
              {suggestion}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg">
        <p className="text-sm text-gray-700">
          <strong>💼 Pro Tip:</strong> Tailor your resume to match the job description by incorporating 
          the suggested skills and keywords naturally. Focus on quantifiable achievements and 
          use action verbs to describe your experience.
        </p>
      </div>
    </div>
  );
}

export default SuggestionsList;
