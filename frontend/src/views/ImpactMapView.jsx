import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.heat';

// Get API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL || '';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom marker icons based on category
const createCategoryIcon = (category) => {
  const colors = {
    pothole: '#ef4444',
    garbage: '#f97316',
    vandalism: '#6366f1',
    flood: '#06b6d4',
    infrastructure: '#eab308',
    default: '#3b82f6'
  };
  
  const color = colors[category?.toLowerCase()] || colors.default;
  
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background-color: ${color}; width: 24px; height: 24px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -12]
  });
};

// Heatmap layer component
const HeatmapLayer = ({ issues }) => {
  const map = useMap();

  useEffect(() => {
    if (!issues || issues.length === 0) return;

    // Create heatmap data: [lat, lng, intensity]
    const heatData = issues.map(issue => [
      issue.latitude,
      issue.longitude,
      issue.upvotes ? Math.min(issue.upvotes / 10, 1) : 0.5 // Normalize intensity
    ]);

    // Create heatmap layer
    const heat = L.heatLayer(heatData, {
      radius: 25,
      blur: 15,
      maxZoom: 17,
      max: 1.0,
      gradient: {
        0.0: 'blue',
        0.5: 'lime',
        0.7: 'yellow',
        1.0: 'red'
      }
    }).addTo(map);

    return () => {
      map.removeLayer(heat);
    };
  }, [issues, map]);

  return null;
};

const ImpactMapView = ({ setView }) => {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showHeatmap, setShowHeatmap] = useState(true);

  // Default center: India (approximate center)
  const defaultCenter = [20.5937, 78.9629];
  const defaultZoom = 5;

  useEffect(() => {
    fetchIssues();
  }, []);

  const fetchIssues = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/issues/map`);
      if (!response.ok) throw new Error('Failed to fetch issues');
      const data = await response.json();
      setIssues(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching issues:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-6 border-t pt-4">
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-xl font-semibold">Impact Map Dashboard</h2>
          <button
            onClick={() => setView('home')}
            className="text-blue-600 hover:underline text-sm"
          >
            &larr; Back to Home
          </button>
        </div>
        <p className="text-gray-600 text-sm mb-3">
          Real-time view of civic issues reported across India
        </p>
        
        {/* Heatmap Toggle */}
        <div className="flex items-center gap-2 mb-3">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={showHeatmap}
              onChange={(e) => setShowHeatmap(e.target.checked)}
              className="mr-2"
            />
            <span className="text-sm font-medium">Show Heatmap</span>
          </label>
          <span className="text-xs text-gray-500">({issues.length} issues)</span>
        </div>

        {/* Category Legend */}
        <div className="flex flex-wrap gap-2 text-xs mb-3">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span>Pothole</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span>Garbage</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-indigo-500"></div>
            <span>Vandalism</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-cyan-500"></div>
            <span>Flood</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span>Infrastructure</span>
          </div>
        </div>
      </div>

      {loading && (
        <div className="flex justify-center items-center h-96">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm mb-4">
          Error loading map: {error}
        </div>
      )}

      {!loading && !error && (
        <div className="rounded-lg overflow-hidden border border-gray-200 shadow-sm">
          <MapContainer
            center={defaultCenter}
            zoom={defaultZoom}
            style={{ height: '500px', width: '100%' }}
            scrollWheelZoom={true}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {/* Heatmap Layer */}
            {showHeatmap && <HeatmapLayer issues={issues} />}
            
            {/* Individual Markers */}
            {issues.map((issue) => (
              <Marker
                key={issue.id}
                position={[issue.latitude, issue.longitude]}
                icon={createCategoryIcon(issue.category)}
              >
                <Popup>
                  <div className="min-w-[200px]">
                    <h3 className="font-semibold text-sm mb-1 capitalize">
                      {issue.category}
                    </h3>
                    <p className="text-xs text-gray-700 mb-2">
                      {issue.description}
                    </p>
                    {issue.location && (
                      <p className="text-xs text-gray-500 mb-1">
                        📍 {issue.location}
                      </p>
                    )}
                    <div className="flex justify-between items-center text-xs text-gray-500 mt-2">
                      <span className={`px-2 py-0.5 rounded ${
                        issue.status === 'open' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
                      }`}>
                        {issue.status}
                      </span>
                      <span>👍 {issue.upvotes}</span>
                    </div>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      )}

      {!loading && !error && issues.length === 0 && (
        <div className="text-center text-gray-500 py-8">
          No issues with location data found yet.
        </div>
      )}
    </div>
  );
};

export default ImpactMapView;
