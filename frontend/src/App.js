import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import CloudinaryManager from './CloudinaryManager';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [detectionResults, setDetectionResults] = useState(null);
  const [authenticityResults, setAuthenticityResults] = useState(null);
  const [panAuthenticityResults, setPanAuthenticityResults] = useState(null);
  const [enhancedPanAuthenticityResults, setEnhancedPanAuthenticityResults] = useState(null);
  const [dlAuthenticityResults, setDlAuthenticityResults] = useState(null);
  const [geminiVerificationResults, setGeminiVerificationResults] = useState(null);
  const [openaiVerificationResults, setOpenaiVerificationResults] = useState(null);
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [cloudinaryLoading, setCloudinaryLoading] = useState(false);
  const [cloudinaryError, setCloudinaryError] = useState(null);
  const [originalImage, setOriginalImage] = useState(null);
  const [activeTab, setActiveTab] = useState('aadhaar-detection'); // 'aadhaar-detection', 'aadhaar-authenticity', 'pan-authenticity', 'enhanced-pan-authenticity', 'voter-id-authenticity', 'gemini-verification', 'openai-verification', or 'cloudinary-storage'

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
      setOriginalImage(URL.createObjectURL(acceptedFiles[0]));
      setDetectionResults(null);
      setAuthenticityResults(null);
      setPanAuthenticityResults(null);
      setEnhancedPanAuthenticityResults(null);
      setDlAuthenticityResults(null);
      setGeminiVerificationResults(null);
      setOpenaiVerificationResults(null);
      setError(null);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  });

  const handleDetect = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/detect', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setDetectionResults(result);
    } catch (err) {
      setError('Error detecting entities: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyAuthenticity = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/verify_aadhaar_authenticity', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setAuthenticityResults(result);
    } catch (err) {
      setError('Error verifying authenticity: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyPanAuthenticity = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/verify_pan_authenticity', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setPanAuthenticityResults(result);
    } catch (err) {
      setError('Error verifying PAN authenticity: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyEnhancedPanAuthenticity = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/verify_enhanced_pan_authenticity', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setEnhancedPanAuthenticityResults(result);
    } catch (err) {
      setError('Error verifying PAN authenticity: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyVoterIdAuthenticity = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/verify_voter_id_authenticity', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setDlAuthenticityResults(result); // Reusing this state variable for simplicity
    } catch (err) {
      setError('Error verifying Voter ID authenticity: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Add new function for OpenAI verification
  const handleVerifyWithOpenAI = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/verify_document_with_openai', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const result = await response.json();
      setOpenaiVerificationResults(result);
    } catch (err) {
      console.error('Error verifying with OpenAI/GitHub AI:', err);
      
      // Check if it's a model access error
      if (err.message.includes('no_access') && err.message.includes('model')) {
        setError('Model access error: Your GitHub token may not have access to the requested AI model. Please check your GitHub AI model marketplace subscription or contact support.');
      } else {
        setError('Error verifying with OpenAI/GitHub AI: ' + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  // Add new function for Gemini verification
  const handleVerifyWithGemini = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/verify_document_with_gemini', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const result = await response.json();
      setGeminiVerificationResults(result);
    } catch (err) {
      console.error('Error verifying with Gemini:', err);
      setError('Error verifying with Gemini: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Function to get class name based on class_id
  const getClassName = (classId) => {
    const classNames = {
      0: 'Aadhaar Number',
      1: 'Name Field',
      2: 'Date of Birth',
      3: 'Address Field',
      4: 'Photo Area'
    };
    return classNames[classId] || `Entity ${classId}`;
  };

  // Function to get color based on class_id
  const getClassColor = (classId) => {
    const colors = {
      0: 'bg-blue-100 border-blue-500',
      1: 'bg-green-100 border-green-500',
      2: 'bg-yellow-100 border-yellow-500',
      3: 'bg-purple-100 border-purple-500',
      4: 'bg-pink-100 border-pink-500'
    };
    return colors[classId] || 'bg-gray-100 border-gray-500';
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Document Verification System</h1>
          <p className="text-lg text-gray-600 mb-8">
            Upload Aadhaar, PAN, or Voter ID images to detect entities or verify authenticity
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 mb-6">
          <button
            className={`py-2 px-4 font-medium text-sm ${activeTab === 'aadhaar-detection' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('aadhaar-detection')}
          >
            Aadhaar Detection
          </button>
          <button
            className={`py-2 px-4 font-medium text-sm ${activeTab === 'aadhaar-authenticity' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('aadhaar-authenticity')}
          >
            Aadhaar Authenticity
          </button>
          <button
            className={`py-2 px-4 font-medium text-sm ${activeTab === 'pan-authenticity' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('pan-authenticity')}
          >
            PAN Authenticity
          </button>
          <button
            className={`py-2 px-4 font-medium text-sm ${activeTab === 'enhanced-pan-authenticity' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('enhanced-pan-authenticity')}
          >
            Enhanced PAN
          </button>
          <button
            className={`py-2 px-4 font-medium text-sm ${activeTab === 'voter-id-authenticity' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('voter-id-authenticity')}
          >
            Voter ID
          </button>
          {/* Add All Documents Verification tab */}
          <button
            className={`py-2 px-4 font-medium text-sm ${activeTab === 'gemini-verification' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('gemini-verification')}
          >
            All Documents Verification
          </button>
          {/* Add OpenAI Verification tab */}
          <button
            className={`py-2 px-4 font-medium text-sm ${activeTab === 'openai-verification' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('openai-verification')}
          >
            OpenAI Verification
          </button>
        </div>

        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="px-6 py-8">
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
                isDragActive
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <input {...getInputProps()} />
              {selectedFile ? (
                <div>
                  <p className="text-lg font-medium text-gray-900 mb-2">
                    Selected file: {selectedFile.name}
                  </p>
                  <p className="text-sm text-gray-500">
                    Click or drag to select a different file
                  </p>
                </div>
              ) : (
                <div>
                  <svg
                    className="mx-auto h-12 w-12 text-gray-400"
                    stroke="currentColor"
                    fill="none"
                    viewBox="0 0 48 48"
                    aria-hidden="true"
                  >
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      strokeWidth={2}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  <p className="mt-2 text-lg font-medium text-gray-900">
                    {activeTab === 'voter-id-authenticity' 
                      ? 'Drag and drop a Voter ID image here' 
                      : activeTab === 'pan-authenticity' 
                      ? 'Drag and drop a PAN card image here' 
                      : activeTab === 'gemini-verification'
                      ? 'Drag and drop any document image here'
                      : 'Drag and drop an Aadhaar card image here'}
                  </p>
                  <p className="mt-1 text-sm text-gray-500">
                    or click to select a file
                  </p>
                  <p className="mt-1 text-xs text-gray-400">
                    PNG, JPG, JPEG up to 10MB
                  </p>
                </div>
              )}
            </div>

            {selectedFile && (
              <div className="mt-6 flex flex-col sm:flex-row justify-center gap-4">
                {activeTab === 'aadhaar-detection' && (
                  <button
                    onClick={handleDetect}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Detecting Entities...
                      </>
                    ) : (
                      'Detect Aadhaar Entities'
                    )}
                  </button>
                )}
                
                {activeTab === 'aadhaar-authenticity' && (
                  <button
                    onClick={handleVerifyAuthenticity}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Verifying...
                      </>
                    ) : (
                      'Verify Aadhaar Authenticity'
                    )}
                  </button>
                )}
                
                {activeTab === 'pan-authenticity' && (
                  <button
                    onClick={handleVerifyPanAuthenticity}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Verifying...
                      </>
                    ) : (
                      'Verify PAN Authenticity'
                    )}
                  </button>
                )}
                
                {activeTab === 'enhanced-pan-authenticity' && (
                  <button
                    onClick={handleVerifyEnhancedPanAuthenticity}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Verifying...
                      </>
                    ) : (
                      'Verify Enhanced PAN Authenticity'
                    )}
                  </button>
                )}
                
                {activeTab === 'voter-id-authenticity' && (
                  <button
                    onClick={handleVerifyVoterIdAuthenticity}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Verifying...
                      </>
                    ) : (
                      'Verify Voter ID Authenticity'
                    )}
                  </button>
                )}

                {/* Add Gemini Verification button */}
                {activeTab === 'gemini-verification' && (
                  <button
                    onClick={handleVerifyWithGemini}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Analyzing document...
                      </>
                    ) : (
                      'Verify Document with AI'
                    )}
                  </button>
                )}
                
                {/* Add OpenAI Verification button */}
                {activeTab === 'openai-verification' && (
                  <button
                    onClick={handleVerifyWithOpenAI}
                    disabled={loading}
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Analyzing document...
                      </>
                    ) : (
                      'Verify Document with OpenAI/GitHub AI'
                    )}
                  </button>
                )}
              </div>
            )}

            {error && (
              <div className="mt-6 p-4 bg-red-50 rounded-md">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg
                      className="h-5 w-5 text-red-400"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                      aria-hidden="true"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Display original image */}
            {originalImage && (
              <div className="mt-8">
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {activeTab === 'dl-authenticity' 
                    ? 'Driving License Image' 
                    : activeTab === 'enhanced-pan-authenticity' || activeTab === 'pan-authenticity'
                    ? 'PAN Card Image' 
                    : 'Aadhaar Card Image'}
                </h3>
                <div className="border rounded-lg overflow-hidden">
                  <img 
                    src={originalImage} 
                    alt={activeTab === 'dl-authenticity' 
                      ? 'Driving License' 
                      : activeTab === 'enhanced-pan-authenticity' || activeTab === 'pan-authenticity'
                      ? 'PAN Card' 
                      : 'Aadhaar Card'} 
                    className="max-w-full h-auto max-h-96 mx-auto"
                  />
                </div>
              </div>
            )}

            {detectionResults && activeTab === 'aadhaar-detection' && (
              <div className="mt-8 bg-gray-50 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Detection Results</h2>
                
                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Total Entities Detected</p>
                      <p className="text-2xl font-bold text-indigo-600">{detectionResults.total_detections}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Image Size</p>
                      <p className="text-2xl font-bold text-indigo-600">{detectionResults.image_width}×{detectionResults.image_height}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Model Used</p>
                      <p className="text-2xl font-bold text-indigo-600">YOLOv8</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Average Confidence</p>
                      <p className="text-2xl font-bold text-indigo-600">
                        {detectionResults.detected_entities.length > 0 
                          ? (detectionResults.detected_entities.reduce((sum, entity) => sum + entity.confidence, 0) / detectionResults.detected_entities.length * 100).toFixed(1) + '%'
                          : '0%'}
                      </p>
                    </div>
                  </div>
                </div>

                {detectionResults.detected_entities.length > 0 && (
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Detected Entities</h3>
                    <div className="space-y-4">
                      {detectionResults.detected_entities.map((entity, index) => (
                        <div 
                          key={index} 
                          className={`border-l-4 p-4 rounded-r ${getClassColor(entity.class_id)}`}
                        >
                          <div className="flex justify-between items-center">
                            <h4 className="font-medium text-gray-900">{getClassName(entity.class_id)}</h4>
                            <span className="text-sm font-medium text-gray-700">
                              {(entity.confidence * 100).toFixed(1)}% confidence
                            </span>
                          </div>
                          <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
                            <div>Position: ({entity.x_min.toFixed(0)}, {entity.y_min.toFixed(0)})</div>
                            <div>Size: {entity.width.toFixed(0)}×{entity.height.toFixed(0)} pixels</div>
                            <div>Center: ({entity.x_center.toFixed(0)}, {entity.y_center.toFixed(0)})</div>
                            <div>Area: {(entity.width * entity.height).toFixed(0)} pixels²</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {detectionResults.detected_entities.length === 0 && (
                  <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <p className="text-sm text-yellow-700">
                          No entities were detected in this Aadhaar card image. Please ensure the image is clear and properly aligned.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {authenticityResults && activeTab === 'aadhaar-authenticity' && (
              <div className="mt-8 bg-gray-50 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Aadhaar Authenticity Verification</h2>
                
                <div className="mb-6">
                  <div className={`p-4 rounded-lg ${authenticityResults.is_authentic ? 'bg-green-100 border border-green-300' : 'bg-red-100 border border-red-300'}`}>
                    <div className="flex items-center">
                      {authenticityResults.is_authentic ? (
                        <svg className="h-8 w-8 text-green-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-8 w-8 text-red-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {authenticityResults.is_authentic ? 'Authentic Aadhaar Card' : 'Potentially Fake Aadhaar Card'}
                        </h3>
                        <p className="text-sm text-gray-700">
                          Confidence: {(authenticityResults.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Emblem Detected</p>
                      <p className={`text-2xl font-bold ${authenticityResults.emblem_detected ? 'text-green-600' : 'text-red-600'}`}>
                        {authenticityResults.emblem_detected ? 'Yes' : 'No'}
                      </p>
                      {authenticityResults.emblem_detected && (
                        <p className="text-sm text-gray-600 mt-1">
                          Confidence: {(authenticityResults.emblem_confidence || 0 * 100).toFixed(1)}%
                        </p>
                      )}
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Government Text Detected</p>
                      <p className={`text-2xl font-bold ${authenticityResults.government_text_detected ? 'text-green-600' : 'text-red-600'}`}>
                        {authenticityResults.government_text_detected ? 'Yes' : 'No'}
                      </p>
                      {authenticityResults.government_text_detected && (
                        <p className="text-sm text-gray-600 mt-1">
                          Confidence: {(authenticityResults.government_text_confidence || 0 * 100).toFixed(1)}%
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Detection Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Total Entities Detected</p>
                      <p className="text-2xl font-bold text-indigo-600">{authenticityResults.total_detections}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Model Used</p>
                      <p className="text-2xl font-bold text-indigo-600">YOLOv8</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Verification Method</p>
                      <p className="text-2xl font-bold text-indigo-600">Visual Analysis</p>
                    </div>
                  </div>
                </div>

                {authenticityResults.detected_entities.length > 0 && (
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Detected Entities</h3>
                    <div className="space-y-4">
                      {authenticityResults.detected_entities.map((entity, index) => (
                        <div 
                          key={index} 
                          className={`border-l-4 p-4 rounded-r ${getClassColor(entity.class_id)}`}
                        >
                          <div className="flex justify-between items-center">
                            <h4 className="font-medium text-gray-900">{getClassName(entity.class_id)}</h4>
                            <span className="text-sm font-medium text-gray-700">
                              {(entity.confidence * 100).toFixed(1)}% confidence
                            </span>
                          </div>
                          <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
                            <div>Position: ({entity.x_min.toFixed(0)}, {entity.y_min.toFixed(0)})</div>
                            <div>Size: {entity.width.toFixed(0)}×{entity.height.toFixed(0)} pixels</div>
                            <div>Center: ({entity.x_center.toFixed(0)}, {entity.y_center.toFixed(0)})</div>
                            <div>Area: {(entity.width * entity.height).toFixed(0)} pixels²</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {panAuthenticityResults && activeTab === 'pan-authenticity' && (
              <div className="mt-8 bg-gray-50 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">PAN Card Authenticity Verification</h2>
                
                <div className="mb-6">
                  <div className={`p-4 rounded-lg ${panAuthenticityResults.is_authentic ? 'bg-green-100 border border-green-300' : 'bg-red-100 border border-red-300'}`}>
                    <div className="flex items-center">
                      {panAuthenticityResults.is_authentic ? (
                        <svg className="h-8 w-8 text-green-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-8 w-8 text-red-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {panAuthenticityResults.is_authentic ? 'Authentic PAN Card' : 'Potentially Fake PAN Card'}
                        </h3>
                        <p className="text-sm text-gray-700">
                          Confidence: {(panAuthenticityResults.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">PAN Pattern Detected</p>
                      <p className={`text-2xl font-bold ${panAuthenticityResults.pan_pattern_detected ? 'text-green-600' : 'text-red-600'}`}>
                        {panAuthenticityResults.pan_pattern_detected ? 'Yes' : 'No'}
                      </p>
                      {panAuthenticityResults.pan_pattern_detected && (
                        <p className="text-sm text-gray-600 mt-1">
                          Confidence: {(panAuthenticityResults.pan_pattern_confidence || 0 * 100).toFixed(1)}%
                        </p>
                      )}
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">PAN Text Detected</p>
                      <p className={`text-2xl font-bold ${panAuthenticityResults.pan_text_detected ? 'text-green-600' : 'text-red-600'}`}>
                        {panAuthenticityResults.pan_text_detected ? 'Yes' : 'No'}
                      </p>
                      {panAuthenticityResults.pan_text_detected && (
                        <p className="text-sm text-gray-600 mt-1">
                          Confidence: {(panAuthenticityResults.pan_text_confidence || 0 * 100).toFixed(1)}%
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Detection Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Total Entities Detected</p>
                      <p className="text-2xl font-bold text-indigo-600">{panAuthenticityResults.total_detections}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Model Used</p>
                      <p className="text-2xl font-bold text-indigo-600">YOLOv8</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Verification Method</p>
                      <p className="text-2xl font-bold text-indigo-600">Pattern & Text Analysis</p>
                    </div>
                  </div>
                </div>

                {panAuthenticityResults.detected_entities.length > 0 && (
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Detected Entities</h3>
                    <div className="space-y-4">
                      {panAuthenticityResults.detected_entities.map((entity, index) => (
                        <div 
                          key={index} 
                          className={`border-l-4 p-4 rounded-r ${getClassColor(entity.class_id)}`}
                        >
                          <div className="flex justify-between items-center">
                            <h4 className="font-medium text-gray-900">{getClassName(entity.class_id)}</h4>
                            <span className="text-sm font-medium text-gray-700">
                              {(entity.confidence * 100).toFixed(1)}% confidence
                            </span>
                          </div>
                          <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
                            <div>Position: ({entity.x_min.toFixed(0)}, {entity.y_min.toFixed(0)})</div>
                            <div>Size: {entity.width.toFixed(0)}×{entity.height.toFixed(0)} pixels</div>
                            <div>Center: ({entity.x_center.toFixed(0)}, {entity.y_center.toFixed(0)})</div>
                            <div>Area: {(entity.width * entity.height).toFixed(0)} pixels²</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {enhancedPanAuthenticityResults && activeTab === 'enhanced-pan-authenticity' && (
              <div className="mt-8 bg-gray-50 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Enhanced PAN Card Verification</h2>
                
                <div className="mb-6">
                  <div className={`p-4 rounded-lg ${enhancedPanAuthenticityResults.is_authentic ? 'bg-green-100 border border-green-300' : 'bg-red-100 border border-red-300'}`}>
                    <div className="flex items-center">
                      {enhancedPanAuthenticityResults.is_authentic ? (
                        <svg className="h-8 w-8 text-green-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-8 w-8 text-red-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {enhancedPanAuthenticityResults.is_authentic ? 'Authentic PAN Card' : 'Potentially Fake PAN Card'}
                        </h3>
                        <p className="text-sm text-gray-700">
                          Confidence: {(enhancedPanAuthenticityResults.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Layout Verified</p>
                      <p className={`text-2xl font-bold ${enhancedPanAuthenticityResults.layout_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {enhancedPanAuthenticityResults.layout_verified ? 'Yes' : 'No'}
                      </p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Text Validated</p>
                      <p className={`text-2xl font-bold ${enhancedPanAuthenticityResults.text_validated ? 'text-green-600' : 'text-red-600'}`}>
                        {enhancedPanAuthenticityResults.text_validated ? 'Yes' : 'No'}
                      </p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Security Features</p>
                      <p className={`text-2xl font-bold ${enhancedPanAuthenticityResults.security_features_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {enhancedPanAuthenticityResults.security_features_verified ? 'Yes' : 'No'}
                      </p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Issuer Verified</p>
                      <p className={`text-2xl font-bold ${enhancedPanAuthenticityResults.issuer_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {enhancedPanAuthenticityResults.issuer_verified ? 'Yes' : 'No'}
                      </p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Tampering Detected</p>
                      <p className={`text-2xl font-bold ${!enhancedPanAuthenticityResults.tampering_detected ? 'text-green-600' : 'text-red-600'}`}>
                        {!enhancedPanAuthenticityResults.tampering_detected ? 'No' : 'Yes'}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Extracted Information</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">PAN Number</p>
                      <p className="text-lg font-bold text-gray-900">{enhancedPanAuthenticityResults.pan_number || 'Not detected'}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Holder Name</p>
                      <p className="text-lg font-bold text-gray-900">{enhancedPanAuthenticityResults.holder_name || 'Not detected'}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Father's Name</p>
                      <p className="text-lg font-bold text-gray-900">{enhancedPanAuthenticityResults.fathers_name || 'Not detected'}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Date of Birth</p>
                      <p className="text-lg font-bold text-gray-900">{enhancedPanAuthenticityResults.date_of_birth || 'Not detected'}</p>
                    </div>
                  </div>
                </div>

                {enhancedPanAuthenticityResults.issues_found.length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Issues Found</h3>
                    <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                      <div className="flex">
                        <div className="flex-shrink-0">
                          <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </div>
                        <div className="ml-3">
                          <ul className="text-sm text-yellow-700 list-disc pl-5 space-y-1">
                            {enhancedPanAuthenticityResults.issues_found.map((issue, index) => (
                              <li key={index}>{issue}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Detection Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Total Entities Detected</p>
                      <p className="text-2xl font-bold text-indigo-600">{enhancedPanAuthenticityResults.total_detections}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Model Used</p>
                      <p className="text-2xl font-bold text-indigo-600">YOLOv8 + Enhanced Verification</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Verification Method</p>
                      <p className="text-2xl font-bold text-indigo-600">Comprehensive Analysis</p>
                    </div>
                  </div>
                </div>

                {enhancedPanAuthenticityResults.detected_entities.length > 0 && (
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Detected Entities</h3>
                    <div className="space-y-4">
                      {enhancedPanAuthenticityResults.detected_entities.map((entity, index) => (
                        <div 
                          key={index} 
                          className={`border-l-4 p-4 rounded-r ${getClassColor(entity.class_id)}`}
                        >
                          <div className="flex justify-between items-center">
                            <h4 className="font-medium text-gray-900">{getClassName(entity.class_id)}</h4>
                            <span className="text-sm font-medium text-gray-700">
                              {(entity.confidence * 100).toFixed(1)}% confidence
                            </span>
                          </div>
                          <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
                            <div>Position: ({entity.x_min.toFixed(0)}, {entity.y_min.toFixed(0)})</div>
                            <div>Size: {entity.width.toFixed(0)}×{entity.height.toFixed(0)} pixels</div>
                            <div>Center: ({entity.x_center.toFixed(0)}, {entity.y_center.toFixed(0)})</div>
                            <div>Area: {(entity.width * entity.height).toFixed(0)} pixels²</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {dlAuthenticityResults && activeTab === 'voter-id-authenticity' && (
              <div className="mt-8 bg-gray-50 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Voter ID Authenticity Verification</h2>
                
                <div className="mb-6">
                  <div className={`p-4 rounded-lg ${dlAuthenticityResults.is_authentic ? 'bg-green-100 border border-green-300' : 'bg-red-100 border border-red-300'}`}>
                    <div className="flex items-center">
                      {dlAuthenticityResults.is_authentic ? (
                        <svg className="h-8 w-8 text-green-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-8 w-8 text-red-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {dlAuthenticityResults.is_authentic ? 'Authentic Voter ID' : 'Potentially Fake Voter ID'}
                        </h3>
                        <p className="text-sm text-gray-700">
                          Confidence: {(dlAuthenticityResults.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Document Layout</p>
                      <p className={`text-2xl font-bold ${dlAuthenticityResults.layout_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {dlAuthenticityResults.layout_verified ? 'Verified' : 'Not Verified'}
                      </p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Security Features</p>
                      <p className={`text-2xl font-bold ${dlAuthenticityResults.security_features_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {dlAuthenticityResults.security_features_verified ? 'Verified' : 'Not Verified'}
                      </p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Text Quality</p>
                      <p className={`text-2xl font-bold ${dlAuthenticityResults.text_quality_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {dlAuthenticityResults.text_quality_verified ? 'Verified' : 'Not Verified'}
                      </p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">EPIC Number</p>
                      <p className={`text-2xl font-bold ${dlAuthenticityResults.epic_number_valid ? 'text-green-600' : 'text-red-600'}`}>
                        {dlAuthenticityResults.epic_number_valid ? 'Valid' : 'Invalid'}
                      </p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Photo Quality</p>
                      <p className={`text-2xl font-bold ${dlAuthenticityResults.photo_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {dlAuthenticityResults.photo_verified ? 'Verified' : 'Not Verified'}
                      </p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Data Consistency</p>
                      <p className={`text-2xl font-bold ${dlAuthenticityResults.data_consistency_verified ? 'text-green-600' : 'text-red-600'}`}>
                        {dlAuthenticityResults.data_consistency_verified ? 'Verified' : 'Not Verified'}
                      </p>
                    </div>
                  </div>
                </div>
                
                {dlAuthenticityResults.issues_found.length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Issues Found</h3>
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <ul className="list-disc pl-5 space-y-1">
                        {dlAuthenticityResults.issues_found.map((issue, index) => (
                          <li key={index} className="text-yellow-700">{issue}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
                
                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Extracted Information</h3>
                  <div className="bg-white rounded-lg shadow overflow-hidden">
                    <table className="min-w-full divide-y divide-gray-200">
                      <tbody className="bg-white divide-y divide-gray-200">
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500">EPIC Number</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{dlAuthenticityResults.epic_number || 'Not detected'}</td>
                        </tr>
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500">Voter Name</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{dlAuthenticityResults.voter_name || 'Not detected'}</td>
                        </tr>
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500">Father's Name</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{dlAuthenticityResults.fathers_name || 'Not detected'}</td>
                        </tr>
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500">Date of Birth</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{dlAuthenticityResults.date_of_birth || 'Not detected'}</td>
                        </tr>
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500">Gender</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{dlAuthenticityResults.gender || 'Not detected'}</td>
                        </tr>
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500">Address</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{dlAuthenticityResults.address || 'Not detected'}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Detection Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Total Entities Detected</p>
                      <p className="text-2xl font-bold text-indigo-600">{dlAuthenticityResults.total_detections}</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Model Used</p>
                      <p className="text-2xl font-bold text-indigo-600">YOLOv8</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="text-sm text-gray-500">Verification Method</p>
                      <p className="text-2xl font-bold text-indigo-600">Comprehensive Analysis</p>
                    </div>
                  </div>
                </div>

                {dlAuthenticityResults.detected_entities.length > 0 && (
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Detected Entities</h3>
                    <div className="space-y-4">
                      {dlAuthenticityResults.detected_entities.map((entity, index) => (
                        <div 
                          key={index} 
                          className={`border-l-4 p-4 rounded-r ${getClassColor(entity.class_id)}`}
                        >
                          <div className="flex justify-between items-center">
                            <h4 className="font-medium text-gray-900">{getClassName(entity.class_id)}</h4>
                            <span className="text-sm font-medium text-gray-700">
                              {(entity.confidence * 100).toFixed(1)}% confidence
                            </span>
                          </div>
                          <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
                            <div>Position: ({entity.x_min.toFixed(0)}, {entity.y_min.toFixed(0)})</div>
                            <div>Size: {entity.width.toFixed(0)}×{entity.height.toFixed(0)} pixels</div>
                            <div>Center: ({entity.x_center.toFixed(0)}, {entity.y_center.toFixed(0)})</div>
                            <div>Area: {(entity.width * entity.height).toFixed(0)} pixels²</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Add All Documents Verification Results Section */}
            {geminiVerificationResults && activeTab === 'gemini-verification' && (
              <div className="mt-8 bg-gray-50 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">AI-Powered Document Verification</h2>
                
                <div className="mb-6">
                  <div className={`p-4 rounded-lg ${geminiVerificationResults.is_authentic ? 'bg-green-100 border border-green-300' : 'bg-red-100 border border-red-300'}`}>
                    <div className="flex items-center">
                      {geminiVerificationResults.is_authentic ? (
                        <svg className="h-8 w-8 text-green-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-8 w-8 text-red-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {geminiVerificationResults.is_authentic ? 'Authentic Document' : 'Potentially Fake Document'}
                        </h3>
                        <p className="text-sm text-gray-700">
                          Confidence: {(geminiVerificationResults.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Analysis Explanation</h3>
                  <div className="bg-white p-4 rounded-lg shadow">
                    <p className="text-gray-700 whitespace-pre-wrap">{geminiVerificationResults.explanation}</p>
                  </div>
                </div>

                {geminiVerificationResults.issues_found.length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Issues Found</h3>
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <ul className="list-disc pl-5 space-y-1">
                        {geminiVerificationResults.issues_found.map((issue, index) => (
                          <li key={index} className="text-yellow-700">{issue}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {Object.keys(geminiVerificationResults.extracted_info).length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Extracted Information</h3>
                    <div className="bg-white rounded-lg shadow overflow-hidden">
                      <table className="min-w-full divide-y divide-gray-200">
                        <tbody className="bg-white divide-y divide-gray-200">
                          {Object.entries(geminiVerificationResults.extracted_info).map(([key, value], index) => (
                            <tr key={index}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500 capitalize">{key.replace(/_/g, ' ')}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{String(value)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {geminiVerificationResults.verification_factors.length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Verification Factors Considered</h3>
                    <div className="flex flex-wrap gap-2">
                      {geminiVerificationResults.verification_factors.map((factor, index) => (
                        <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
                          {factor}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {/* Add OpenAI Verification Results Section */}
            {openaiVerificationResults && activeTab === 'openai-verification' && (
              <div className="mt-8 bg-gray-50 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">OpenAI-Powered Document Verification</h2>
                
                <div className="mb-6">
                  <div className={`p-4 rounded-lg ${openaiVerificationResults.is_authentic ? 'bg-green-100 border border-green-300' : 'bg-red-100 border border-red-300'}`}>
                    <div className="flex items-center">
                      {openaiVerificationResults.is_authentic ? (
                        <svg className="h-8 w-8 text-green-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-8 w-8 text-red-600 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {openaiVerificationResults.is_authentic ? 'Authentic Document' : 'Potentially Fake Document'}
                        </h3>
                        <p className="text-sm text-gray-700">
                          Confidence: {(openaiVerificationResults.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="font-medium text-gray-900 mb-2">Analysis Explanation</h3>
                  <div className="bg-white p-4 rounded-lg shadow">
                    <p className="text-gray-700 whitespace-pre-wrap">{openaiVerificationResults.explanation}</p>
                  </div>
                </div>

                {openaiVerificationResults.issues_found.length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Issues Found</h3>
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <ul className="list-disc pl-5 space-y-1">
                        {openaiVerificationResults.issues_found.map((issue, index) => (
                          <li key={index} className="text-yellow-700">{issue}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {Object.keys(openaiVerificationResults.extracted_info).length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Extracted Information</h3>
                    <div className="bg-white rounded-lg shadow overflow-hidden">
                      <table className="min-w-full divide-y divide-gray-200">
                        <tbody className="bg-white divide-y divide-gray-200">
                          {Object.entries(openaiVerificationResults.extracted_info).map(([key, value], index) => (
                            <tr key={index}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500 capitalize">{key.replace(/_/g, ' ')}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{String(value)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {openaiVerificationResults.verification_factors.length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-medium text-gray-900 mb-2">Verification Factors Considered</h3>
                    <div className="flex flex-wrap gap-2">
                      {openaiVerificationResults.verification_factors.map((factor, index) => (
                        <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                          {factor}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>This tool detects entities on Aadhaar, PAN, and Voter ID documents using computer vision. Results may vary based on image quality.</p>
        </div>
      </div>
    </div>
  );
}

export default App;