import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import apiClient from './api';

// Fix the default Leaflet marker icon broken image bug
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Kampala coordinates
const KAMPALA_CENTER = [0.3476, 32.5825];

export default function MapView() {
  const [potholes, setPotholes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPotholes = async () => {
      try {
        setLoading(true);
        const { data } = await apiClient.get('/potholes');
        setPotholes(data || []);
      } catch (err) {
        setError(err.message || 'An error occurred while fetching potholes.');
      } finally {
        setLoading(false);
      }
    };

    fetchPotholes();
  }, []);

  // Parse WKT POINT(lng lat) string into [latitude, longitude]
  const parseLocation = (wktString) => {
    if (!wktString) return null;
    const match = wktString.match(/POINT\s*\(\s*([^ ]+)\s+([^ ]+)\s*\)/i);
    if (match) {
      const lng = parseFloat(match[1]);
      const lat = parseFloat(match[2]);
      if (!isNaN(lng) && !isNaN(lat)) {
        return [lat, lng]; // Leaflet uses [lat, lng]
      }
    }
    return null;
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Unknown Date';
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateStr;
    }
  };

  if (loading) {
    return (
      <div className="map-loader">
        <div className="spinner"></div>
        <p>Loading pothole map...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="map-error">
        <h3>Oops! Something went wrong</h3>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="map-wrapper">
      <div className="map-legend">
        <h4>Uganda Pothole Reports</h4>
        <div className="legend-item">
          <span className="bullet active"></span>
          <span>Active / Unresolved ({potholes.filter(p => p.status !== 'resolved').length})</span>
        </div>
        <div className="legend-item">
          <span className="bullet resolved"></span>
          <span>Resolved ({potholes.filter(p => p.status === 'resolved').length})</span>
        </div>
      </div>
      
      <MapContainer 
        center={KAMPALA_CENTER} 
        zoom={13} 
        scrollWheelZoom={true} 
        className="leaflet-container-fullscreen"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {potholes.map((pothole) => {
          const coords = parseLocation(pothole.location);
          if (!coords) return null;

          return (
            <Marker key={pothole.id} position={coords}>
              <Popup className="pothole-popup">
                <div className="popup-content">
                  {pothole.image_url ? (
                    <img 
                      src={pothole.image_url} 
                      alt="Pothole" 
                      className="popup-image" 
                      loading="lazy"
                    />
                  ) : (
                    <div className="popup-no-image">No Image Available</div>
                  )}
                  <div className="popup-meta">
                    <span className={`status-badge ${pothole.status || 'active'}`}>
                      {pothole.status || 'Active'}
                    </span>
                    <p className="popup-id">ID: {pothole.id}</p>
                    <p className="popup-date">Reported: {formatDate(pothole.created_at)}</p>
                    <p className="popup-coords">
                      Coords: {coords[0].toFixed(5)}, {coords[1].toFixed(5)}
                    </p>
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}
