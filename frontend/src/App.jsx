import React, { useState, useEffect, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import ChatWidget from './components/ChatWidget';

// Lazy Load Views
const Home = React.lazy(() => import('./views/Home'));
const MapView = React.lazy(() => import('./views/MapView'));
const ReportForm = React.lazy(() => import('./views/ReportForm'));
const ActionView = React.lazy(() => import('./views/ActionView'));
const MaharashtraRepView = React.lazy(() => import('./views/MaharashtraRepView'));

// Lazy Load Detectors
const PotholeDetector = React.lazy(() => import('./PotholeDetector'));
const GarbageDetector = React.lazy(() => import('./GarbageDetector'));
const VandalismDetector = React.lazy(() => import('./VandalismDetector'));
const FloodDetector = React.lazy(() => import('./FloodDetector'));
const InfrastructureDetector = React.lazy(() => import('./InfrastructureDetector'));

// Get API URL from environment variable, fallback to relative URL for local dev
const API_URL = import.meta.env.VITE_API_URL || '';

function Layout({ children }) {
    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
            <ChatWidget />
            <div className="bg-white shadow-xl rounded-2xl p-6 max-w-lg w-full mt-6 mb-24 border border-gray-100">
                <header className="text-center mb-6">
                    <Link to="/">
                        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-blue-600 cursor-pointer">
                            VishwaGuru
                        </h1>
                    </Link>
                    <p className="text-gray-500 text-sm mt-1">
                        Empowering Citizens, Solving Problems.
                    </p>
                </header>
                {children}
            </div>
        </div>
    );
}

function App() {
  const [recentIssues, setRecentIssues] = useState([]);

  // Fetch recent issues on mount
  const fetchRecentIssues = async () => {
    try {
      const response = await fetch(`${API_URL}/api/issues/recent`);
      if (response.ok) {
        const data = await response.json();
        setRecentIssues(data);
      }
    } catch (e) {
      console.error("Failed to fetch recent issues", e);
    }
  };

  useEffect(() => {
    fetchRecentIssues();
  }, []);

  const handleUpvote = async (id) => {
    try {
        const response = await fetch(`${API_URL}/api/issues/${id}/vote`, {
            method: 'POST'
        });
        if (response.ok) {
            // Update local state to reflect change immediately (optimistic UI or re-fetch)
            setRecentIssues(prev => prev.map(issue =>
                issue.id === id ? { ...issue, upvotes: (issue.upvotes || 0) + 1 } : issue
            ));
        }
    } catch (e) {
        console.error("Failed to upvote", e);
    }
  };

  return (
    <BrowserRouter>
        <Layout>
            <Suspense fallback={
              <div className="flex justify-center my-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
              </div>
            }>
                <Routes>
                    <Route path="/" element={<Home recentIssues={recentIssues} handleUpvote={handleUpvote} />} />
                    <Route path="/map" element={<MapView />} />
                    <Route path="/report" element={<ReportForm />} />
                    <Route path="/action" element={<ActionView />} />
                    <Route path="/mh-rep" element={<MaharashtraRepView />} />
                    <Route path="/pothole" element={<PotholeDetector />} />
                    <Route path="/garbage" element={<GarbageDetector />} />
                    <Route path="/vandalism" element={<VandalismDetector />} />
                    <Route path="/flood" element={<FloodDetector />} />
                    <Route path="/infrastructure" element={<InfrastructureDetector />} />
                </Routes>
            </Suspense>
        </Layout>
    </BrowserRouter>
  );
}

export default App;
