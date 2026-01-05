import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Get API URL from environment variable, fallback to relative URL for local dev
const API_URL = import.meta.env.VITE_API_URL || '';

const ReportForm = () => {
  const [formData, setFormData] = useState({ description: '', category: 'road', image: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = new FormData();
    payload.append('description', formData.description);
    payload.append('category', formData.category);
    if (formData.image) {
      payload.append('image', formData.image);
    }

    try {
      const response = await fetch(`${API_URL}/api/issues`, {
        method: 'POST',
        body: payload,
      });

      if (!response.ok) throw new Error('Failed to submit issue');

      const data = await response.json();
      // Pass action plan via state
      navigate('/action', { state: { actionPlan: data.action_plan } });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-6">
       <h2 className="text-xl font-semibold mb-4 text-center">Report an Issue</h2>
       {error && <div className="text-red-500 mb-2">{error}</div>}
       <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Category</label>
            <select
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
            >
              <option value="road">Road / Potholes</option>
              <option value="water">Water Supply</option>
              <option value="garbage">Garbage / Sanitation</option>
              <option value="streetlight">Streetlight</option>
              <option value="college_infra">College Infrastructure</option>
              <option value="women_safety">Women Safety</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              rows="3"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Describe the issue..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Photo (Optional)</label>
            <input
              type="file"
              accept="image/*"
              className="mt-1 block w-full text-sm text-gray-500"
              onChange={(e) => setFormData({...formData, image: e.target.files[0]})}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Generate Action Plan'}
          </button>
          <button type="button" onClick={() => navigate('/')} className="mt-2 text-blue-600 underline text-center w-full block">Cancel</button>
       </form>
    </div>
  );
};

export default ReportForm;
