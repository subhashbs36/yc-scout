import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const JsonView: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [jsonData, setJsonData] = useState<string>('{}');

  useEffect(() => {
    // Get data either from route state (direct navigation) or localStorage (new tab)
    const stateData = location.state?.rawJson;
    const localStorageData = localStorage.getItem('rawJsonData');
    
    const rawJson = stateData || localStorageData || '{}';
    setJsonData(rawJson);
    
    // Clear localStorage after retrieving to avoid stale data on future visits
    if (localStorageData) {
      localStorage.removeItem('rawJsonData');
    }
  }, [location]);

  // Format the JSON with proper indentation
  const formattedJson = (() => {
    try {
      return JSON.stringify(JSON.parse(jsonData), null, 2);
    } catch (e) {
      return jsonData; // Return raw if parsing fails
    }
  })();

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">JSON Response Data</h1>
          <button 
            onClick={() => window.close()}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Close
          </button>
        </div>
        <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-auto max-h-[80vh]">
          {formattedJson}
        </pre>
      </div>
    </div>
  );
};

export default JsonView;
