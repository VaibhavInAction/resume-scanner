import React from 'react';

function JDInput({ jobDescription, setJobDescription }) {
  const handleChange = (e) => {
    setJobDescription(e.target.value);
  };

  const loadSample = () => {
    const sampleJD = `Senior Full Stack Developer

We are looking for an experienced Full Stack Developer to join our team.

Requirements:
- 5+ years of experience in full-stack development
- Strong proficiency in JavaScript, React, and Node.js
- Experience with Python and FastAPI
- Knowledge of SQL and NoSQL databases (PostgreSQL, MongoDB)
- Familiarity with cloud platforms (AWS, Azure)
- Experience with CI/CD pipelines and Docker
- Strong problem-solving and communication skills

Nice to have:
- Experience with machine learning and AI
- Knowledge of TypeScript
- Agile/Scrum methodology experience

Education:
- Bachelor's degree in Computer Science or related field`;
    
    setJobDescription(sampleJD);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900">
          💼 Job Description
        </h2>
        <button
          onClick={loadSample}
          className="text-sm text-primary hover:text-blue-700 underline"
        >
          Load Sample
        </button>
      </div>

      <textarea
        value={jobDescription}
        onChange={handleChange}
        placeholder="Paste the job description here...

Include:
• Job title and overview
• Required skills and technologies
• Years of experience needed
• Education requirements
• Responsibilities
• Nice-to-have qualifications"
        className="flex-1 w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
        rows={15}
      />

      <div className="mt-3 flex items-center justify-between text-sm">
        <span className="text-gray-600">
          {jobDescription.length} characters
          {jobDescription.length < 50 && ' (minimum 50 required)'}
        </span>
        {jobDescription.length >= 50 && (
          <span className="text-green-600 font-medium">✓ Ready</span>
        )}
      </div>
    </div>
  );
}

export default JDInput;
