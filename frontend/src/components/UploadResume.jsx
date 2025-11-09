import React, { useRef } from 'react';

function UploadResume({ resumeFile, setResumeFile }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">
        📄 Upload Resume
      </h2>

      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
          resumeFile
            ? 'border-green-400 bg-green-50'
            : 'border-gray-300 bg-gray-50 hover:border-primary hover:bg-blue-50'
        }`}
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.doc,.txt"
          onChange={handleFileChange}
          className="hidden"
        />

        {resumeFile ? (
          <div className="space-y-2">
            <div className="text-4xl">✅</div>
            <p className="text-green-700 font-semibold">{resumeFile.name}</p>
            <p className="text-sm text-gray-600">
              {formatFileSize(resumeFile.size)}
            </p>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setResumeFile(null);
              }}
              className="mt-2 text-sm text-red-600 hover:text-red-700 underline"
            >
              Remove file
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="text-4xl">📁</div>
            <p className="text-gray-700 font-medium">
              Click to upload or drag and drop
            </p>
            <p className="text-sm text-gray-500">
              PDF, DOCX, or TXT (Max 10MB)
            </p>
          </div>
        )}
      </div>

      <div className="mt-4 text-sm text-gray-600">
        <p className="font-medium mb-1">Supported formats:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>PDF (.pdf)</li>
          <li>Microsoft Word (.docx, .doc)</li>
          <li>Plain Text (.txt)</li>
        </ul>
      </div>
    </div>
  );
}

export default UploadResume;
