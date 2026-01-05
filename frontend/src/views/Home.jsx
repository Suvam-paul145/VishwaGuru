import React from 'react';
import {
  AlertTriangle, MapPin, Search, Activity, Camera, Trash2, ThumbsUp,
  Brush, Droplets, Zap, Cat, Flame, Car, Volume2
} from 'lucide-react';

const Home = ({ setView, fetchResponsibilityMap, recentIssues, handleUpvote }) => (
  <div className="space-y-6">
    {/* Quick Actions Grid */}
    <div className="grid grid-cols-3 gap-3">
      <button
        onClick={() => setView('report')}
        className="flex flex-col items-center justify-center bg-blue-50 border-2 border-blue-100 p-2 rounded-xl hover:bg-blue-100 transition shadow-sm h-28"
      >
        <div className="bg-blue-500 text-white p-2 rounded-full mb-1">
          <AlertTriangle size={20} />
        </div>
        <span className="font-semibold text-blue-800 text-xs">Report Issue</span>
      </button>

      <button
        onClick={() => setView('pothole')}
        className="flex flex-col items-center justify-center bg-red-50 border-2 border-red-100 p-2 rounded-xl hover:bg-red-100 transition shadow-sm h-28"
      >
        <div className="bg-red-500 text-white p-2 rounded-full mb-1">
          <Camera size={20} />
        </div>
        <span className="font-semibold text-red-800 text-xs">Detect Pothole</span>
      </button>

      <button
        onClick={() => setView('garbage')}
        className="flex flex-col items-center justify-center bg-orange-50 border-2 border-orange-100 p-2 rounded-xl hover:bg-orange-100 transition shadow-sm h-28"
      >
        <div className="bg-orange-500 text-white p-2 rounded-full mb-1">
          <Trash2 size={20} />
        </div>
        <span className="font-semibold text-orange-800 text-xs">Detect Garbage</span>
      </button>

      <button
        onClick={() => setView('mh-rep')}
        className="flex flex-col items-center justify-center bg-purple-50 border-2 border-purple-100 p-2 rounded-xl hover:bg-purple-100 transition shadow-sm h-28"
      >
        <div className="bg-purple-500 text-white p-2 rounded-full mb-1">
          <Search size={20} />
        </div>
        <span className="font-semibold text-purple-800 text-xs">Find MLA</span>
      </button>

      <button
        onClick={() => setView('vandalism')}
        className="flex flex-col items-center justify-center bg-indigo-50 border-2 border-indigo-100 p-2 rounded-xl hover:bg-indigo-100 transition shadow-sm h-28"
      >
        <div className="bg-indigo-500 text-white p-2 rounded-full mb-1">
          <Brush size={20} />
        </div>
        <span className="font-semibold text-indigo-800 text-xs">Graffiti</span>
      </button>

      <button
        onClick={() => setView('flood')}
        className="flex flex-col items-center justify-center bg-cyan-50 border-2 border-cyan-100 p-2 rounded-xl hover:bg-cyan-100 transition shadow-sm h-28"
      >
        <div className="bg-cyan-500 text-white p-2 rounded-full mb-1">
          <Droplets size={20} />
        </div>
        <span className="font-semibold text-cyan-800 text-xs">Detect Flood</span>
      </button>

      <button
        onClick={() => setView('infrastructure')}
        className="flex flex-col items-center justify-center bg-yellow-50 border-2 border-yellow-100 p-2 rounded-xl hover:bg-yellow-100 transition shadow-sm h-28"
      >
        <div className="bg-yellow-500 text-white p-2 rounded-full mb-1">
          <Zap size={20} />
        </div>
        <span className="font-semibold text-yellow-800 text-xs">Broken Infra</span>
      </button>

      <button
        onClick={() => setView('stray-animal')}
        className="flex flex-col items-center justify-center bg-teal-50 border-2 border-teal-100 p-2 rounded-xl hover:bg-teal-100 transition shadow-sm h-28"
      >
        <div className="bg-teal-500 text-white p-2 rounded-full mb-1">
          <Cat size={20} />
        </div>
        <span className="font-semibold text-teal-800 text-xs">Stray Animal</span>
      </button>

      <button
        onClick={() => setView('fire')}
        className="flex flex-col items-center justify-center bg-rose-50 border-2 border-rose-100 p-2 rounded-xl hover:bg-rose-100 transition shadow-sm h-28"
      >
        <div className="bg-rose-500 text-white p-2 rounded-full mb-1">
          <Flame size={20} />
        </div>
        <span className="font-semibold text-rose-800 text-xs">Fire Alert</span>
      </button>

      <button
        onClick={() => setView('traffic')}
        className="flex flex-col items-center justify-center bg-amber-50 border-2 border-amber-100 p-2 rounded-xl hover:bg-amber-100 transition shadow-sm h-28"
      >
        <div className="bg-amber-500 text-white p-2 rounded-full mb-1">
          <Car size={20} />
        </div>
        <span className="font-semibold text-amber-800 text-xs">Traffic Issue</span>
      </button>

      <button
        onClick={() => setView('noise')}
        className="flex flex-col items-center justify-center bg-lime-50 border-2 border-lime-100 p-2 rounded-xl hover:bg-lime-100 transition shadow-sm h-28"
      >
        <div className="bg-lime-500 text-white p-2 rounded-full mb-1">
          <Volume2 size={20} />
        </div>
        <span className="font-semibold text-lime-800 text-xs">Noise Level</span>
      </button>
    </div>

    <div className="grid grid-cols-1 mt-4">
       <button
        onClick={fetchResponsibilityMap}
        className="flex flex-row items-center justify-center bg-green-50 border-2 border-green-100 p-4 rounded-xl hover:bg-green-100 transition shadow-sm h-16"
      >
        <div className="bg-green-500 text-white p-2 rounded-full mr-3">
          <MapPin size={20} />
        </div>
        <span className="font-semibold text-green-800">Who is Responsible?</span>
      </button>
    </div>

    {/* Recent Activity Feed */}
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-4 border-b border-gray-100 flex items-center gap-2">
        <Activity size={18} className="text-orange-500" />
        <h2 className="font-bold text-gray-800">Community Activity</h2>
      </div>
      <div className="divide-y divide-gray-50 max-h-60 overflow-y-auto">
        {recentIssues.length > 0 ? (
          recentIssues.map((issue) => (
            <div key={issue.id} className="p-3 hover:bg-gray-50 transition">
              <div className="flex justify-between items-start">
                <span className="inline-block px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600 mb-1 capitalize">
                  {issue.category}
                </span>
                <div className="flex items-center gap-2">
                  <button
                      onClick={() => handleUpvote(issue.id)}
                      className="flex items-center gap-1 text-gray-500 hover:text-blue-600 text-xs"
                  >
                      <ThumbsUp size={12} />
                      <span>{issue.upvotes || 0}</span>
                  </button>
                  <span className="text-xs text-gray-400">
                      {new Date(issue.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <p className="text-sm text-gray-700 line-clamp-2">{issue.description}</p>
            </div>
          ))
        ) : (
          <div className="p-4 text-center text-gray-500 text-sm">
            No recent activity to show.
          </div>
        )}
      </div>
    </div>
  </div>
);

export default Home;
