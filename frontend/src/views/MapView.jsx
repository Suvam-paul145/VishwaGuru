import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const API_URL = import.meta.env.VITE_API_URL || '';

const MapView = () => {
    const [responsibilityMap, setResponsibilityMap] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchResponsibilityMap = async () => {
            try {
                const response = await fetch(`${API_URL}/api/responsibility-map`);
                if (!response.ok) throw new Error('Failed to fetch data');
                const data = await response.json();
                setResponsibilityMap(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchResponsibilityMap();
    }, []);

    if (loading) return <div className="text-center mt-10">Loading map...</div>;
    if (error) return <div className="text-center mt-10 text-red-600">{error}</div>;

    return (
      <div className="mt-6 border-t pt-4">
        <h2 className="text-xl font-semibold mb-4 text-center">Responsibility Map</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {responsibilityMap && Object.entries(responsibilityMap).map(([key, value]) => (
            <div key={key} className="bg-gray-50 p-4 rounded shadow-sm border">
              <h3 className="font-bold text-lg capitalize mb-2">{key.replace('_', ' ')}</h3>
              <p className="font-medium text-gray-800">{value.authority}</p>
              <p className="text-sm text-gray-600 mt-1">{value.description}</p>
            </div>
          ))}
        </div>
        <Link to="/" className="mt-6 text-blue-600 underline text-center w-full block">Back to Home</Link>
      </div>
    );
};

export default MapView;
