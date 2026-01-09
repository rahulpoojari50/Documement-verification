import React, { useState } from 'react';

const CloudinaryManager = ({ selectedFile }) => {
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Function to upload a verified document to Cloudinary
  const uploadVerifiedDocument = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/upload_verified_document', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Document uploaded:', result);
      
      // Add to uploaded documents list
      setUploadedDocuments(prev => [...prev, result]);
      
      alert('Document uploaded successfully!');
    } catch (err) {
      console.error('Error uploading document:', err);
      setError(`Error uploading document: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Function to list all documents
  const listDocuments = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/list_documents');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Documents listed:', result);
      
      // Update the uploaded documents list
      setUploadedDocuments(result.resources || []);
    } catch (err) {
      console.error('Error listing documents:', err);
      setError(`Error listing documents: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Function to delete a document
  const deleteDocument = async (publicId) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/delete_document/${publicId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Document deleted:', result);
      
      // Remove from uploaded documents list
      setUploadedDocuments(prev => prev.filter(doc => doc.public_id !== publicId));
      
      alert('Document deleted successfully!');
    } catch (err) {
      console.error('Error deleting document:', err);
      setError(`Error deleting document: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-8 bg-gray-50 rounded-lg p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Cloudinary Document Storage</h2>
      
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <button
          onClick={uploadVerifiedDocument}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Uploading...' : 'Upload Document to Cloudinary'}
        </button>
        
        <button
          onClick={listDocuments}
          disabled={loading}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'List Stored Documents'}
        </button>
      </div>
      
      {uploadedDocuments.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Stored Documents</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {uploadedDocuments.map((doc, index) => (
              <div key={index} className="border rounded-lg p-4 bg-white">
                <img 
                  src={doc.url} 
                  alt="Stored document" 
                  className="w-full h-32 object-cover rounded mb-2"
                />
                <p className="text-xs text-gray-500 truncate">{doc.public_id}</p>
                <div className="mt-2 flex space-x-2">
                  <a 
                    href={doc.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    View
                  </a>
                  <button
                    onClick={() => deleteDocument(doc.public_id)}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CloudinaryManager;