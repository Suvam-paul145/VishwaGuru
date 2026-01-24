import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon in Leaflet + React
// We need to ensure these images are handled correctly by the bundler
// A common workaround is setting the src directly if imports fail, but imports are cleaner
import icon from 'leaflet/dist/images/marker-icon.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Only run this once to fix icons
const fixLeafletIcon = () => {
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
        iconRetinaUrl: iconRetina,
        iconUrl: icon,
        shadowUrl: iconShadow
    });
};

fixLeafletIcon();

const MapView = ({ issues }) => {
    // Filter issues with valid coordinates
    // Ensure latitude and longitude are numbers
    const validIssues = issues.filter(i =>
        i.latitude !== null && i.latitude !== undefined &&
        i.longitude !== null && i.longitude !== undefined
    );

    // Default center (Maharashtra, India)
    const center = [19.7515, 75.7139];

    return (
        <div className="h-[500px] w-full rounded-2xl overflow-hidden shadow-sm border border-gray-100 z-0 relative">
            <MapContainer center={center} zoom={7} style={{ height: '100%', width: '100%' }}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {validIssues.map(issue => (
                    <Marker key={issue.id} position={[issue.latitude, issue.longitude]}>
                        <Popup>
                            <div className="text-sm">
                                <strong className="block mb-1 capitalize text-gray-800">{issue.category}</strong>
                                <p className="mb-1 text-gray-600">{issue.description.substring(0, 50)}{issue.description.length > 50 ? '...' : ''}</p>
                                <span className="text-xs text-gray-400 block">{issue.location || 'Unknown location'}</span>
                                <div className="mt-2 text-xs font-semibold text-blue-600 capitalize">
                                    Status: {issue.status}
                                </div>
                            </div>
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </div>
    );
};

export default MapView;
