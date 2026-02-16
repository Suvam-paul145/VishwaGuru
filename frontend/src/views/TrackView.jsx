import React, { useState } from 'react';
import { ArrowLeft, Search, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { issuesApi } from '../api/issues';

const TrackView = () => {
  const navigate = useNavigate();
  const [issueId, setIssueId] = useState('');
  const [issue, setIssue] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!issueId.trim()) return;

    setLoading(true);
    setError(null);
    setIssue(null);

    try {
      const result = await issuesApi.get(issueId);
      setIssue(result);
    } catch (err) {
      console.error(err);
      setError("Issue not found. Please check the ID.");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'resolved': return 'bg-green-100 text-green-800 border-green-200';
      case 'in_progress': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'rejected': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'resolved': return <CheckCircle size={24} className="text-green-600" />;
      case 'rejected': return <AlertCircle size={24} className="text-red-600" />;
      default: return <Clock size={24} className="text-yellow-600" />;
    }
  };

  return (
    <div className="p-4 max-w-lg mx-auto min-h-screen bg-gray-50">
      <button onClick={() => navigate(-1)} className="flex items-center text-gray-600 mb-6 font-medium hover:text-gray-900 transition">
        <ArrowLeft size={20} className="mr-2" /> Back
      </button>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <h1 className="text-2xl font-bold mb-2 text-gray-900">Track Issue Status</h1>
        <p className="text-gray-500 mb-6 text-sm">Enter your issue ID to see real-time updates.</p>

        <form onSubmit={handleSearch} className="mb-8">
          <div className="relative">
            <input
              type="text"
              value={issueId}
              onChange={(e) => setIssueId(e.target.value)}
              placeholder="e.g., 12345"
              className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition"
            />
            <Search className="absolute left-3 top-3.5 text-gray-400" size={20} />
          </div>
          <button
            type="submit"
            disabled={loading || !issueId}
            className="w-full mt-3 bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
          >
            {loading ? <span className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span> : 'Track Issue'}
          </button>
        </form>

        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-xl text-center border border-red-100 flex items-center justify-center gap-2">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        {issue && (
          <div className="animate-fade-in-up">
            <div className={`p-4 rounded-xl border mb-4 flex items-center justify-between ${getStatusColor(issue.status)}`}>
              <div className="flex items-center gap-3">
                {getStatusIcon(issue.status)}
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide opacity-70">Current Status</p>
                  <p className="font-bold text-lg capitalize">{issue.status.replace('_', ' ')}</p>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Description</label>
                <p className="text-gray-800 font-medium mt-1">{issue.description}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Category</label>
                  <p className="text-gray-800 mt-1 capitalize">{issue.category}</p>
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Location</label>
                  <p className="text-gray-800 mt-1">{issue.location || 'Unknown'}</p>
                </div>
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Reported On</label>
                <p className="text-gray-800 mt-1">{new Date(issue.created_at).toLocaleString()}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrackView;
