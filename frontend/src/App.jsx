
import { useState, useRef, useEffect } from 'react';
import './App.css';
import MapView from './MapView';

function App() {
  const [currentView, setCurrentView] = useState('report'); // 'report' or 'map'
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState('');
  const [ipAddress, setIPAddress] = useState('');
  const [geoInfo, setGeoInfo] = useState({});
  const [locationStatus, setLocationStatus] = useState('');
  const [status, setStatus] = useState('active'); // default to active status
  const fileInputRef = useRef();

  // // Get device location on mount
  // useEffect(() => {
  //   if (navigator.geolocation) {
  //     navigator.geolocation.getCurrentPosition(
  //       (position) => {
  //         const { latitude, longitude } = position.coords;
  //         setLocation(`POINT(${longitude} ${latitude})`);
  //       },
  //       (error) => {
  //         setLocation('');
  //       }
  //     );
  //   }
  // }, []);

 



  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setResult('');
    }
  };
  const handleGetLocation = () => {
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      setLocation(`POINT(${longitude} ${latitude})`);
      setLocationStatus('✅ Location captured');
    },
    (error) => {
      setLocationStatus('❌ Location failed: ' + error.message);
      console.log(error.code, error.message);
    },
    {
      enableHighAccuracy: false,
      timeout: 10000,
      maximumAge: 60000
    }
  );
};

  // Send image and form data to backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedImage) return;
    setLoading(true);
    setResult('');
    const formData = new FormData();
    formData.append('file', selectedImage);
    formData.append('location', location);
    formData.append('status', status);
    formData.append('file_path', ''); // Not used when uploading file directly
    try {
      const response = await fetch('http://localhost:8000/master_upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data.message || 'No result');
    } catch (err) {
      setResult(err.message || 'Error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`app-container ${currentView === 'map' ? 'full-screen-map' : ''}`}>
      <header className="app-header">
        <h1 className="logo-title">StreetWatch</h1>
        <div className="nav-tabs">
          <button 
            className={`nav-tab ${currentView === 'report' ? 'active' : ''}`}
            onClick={() => setCurrentView('report')}
          >
            Report Pothole
          </button>
          <button 
            className={`nav-tab ${currentView === 'map' ? 'active' : ''}`}
            onClick={() => setCurrentView('map')}
          >
            Pothole Map
          </button>
        </div>
      </header>

      <main className="main-content">
        {currentView === 'report' ? (
          <div className="report-container">
            <h2>Report a Street Pothole</h2>
            <p className="subtitle">Help clean up Uganda's streets by reporting road hazards instantly.</p>
            
            <form onSubmit={handleSubmit} className="upload-form">
              <input
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleFileChange}
                ref={fileInputRef}
                style={{ display: 'none' }}
              />
              
              <div className="upload-card" onClick={() => fileInputRef.current.click()}>
                {preview ? (
                  <div className="preview-container">
                    <img src={preview} alt="Preview" className="upload-preview" />
                    <div className="change-photo-badge">Tap to Change</div>
                  </div>
                ) : (
                  <div className="upload-placeholder">
                    <svg className="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>Upload / Take Photo</span>
                  </div>
                )}
              </div>

              <div className="input-group">
                <label>Detected Location</label>
                <div className="input-with-button">
                  <input
                    type="text"
                    placeholder="Fetching GPS location..."
                    value={location}
                    readOnly
                    required
                  />
                  <button 
                    type="button" 
                    className="get-location-btn"
                    onClick={handleGetLocation}
                  >
                    📍 Get Current Location
                  </button>
                </div>
                {locationStatus && <p className="location-status-text">{locationStatus}</p>}
              </div>

              <div className="input-group">
                <label>Report Status</label>
                <select 
                  value={status} 
                  onChange={e => setStatus(e.target.value)}
                  className="status-select"
                  required
                >
                  <option value="active">Active / Unresolved</option>
                  <option value="resolved">Resolved</option>
                </select>
              </div>

              <button 
                type="submit" 
                className="submit-btn" 
                disabled={!selectedImage || loading}
              >
                {loading ? (
                  <span className="btn-loading">
                    <span className="spinner-small"></span> Analyzing Pothole...
                  </span>
                ) : 'Submit Report'}
              </button>
              
              
            </form>
            {result && <div className="result-alert">{result}</div>}
          </div>
          
        ) : (
          <MapView />
        )}
      </main>
    </div>
  );
}

export default App;
