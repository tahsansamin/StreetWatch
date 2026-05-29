
import { useState, useRef, useEffect } from 'react';
import './App.css';


function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState('');
  const [status, setStatus] = useState('');
  const fileInputRef = useRef();


  // Get device location on mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setLocation(`POINT(${longitude} ${latitude})`);
        },
        (error) => {
          setLocation('');
        }
      );
    }
  }, []);

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setResult('');
    }
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
    <div className="container">
      <h1>Pothole Detector</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleFileChange}
          ref={fileInputRef}
        />
        <button
          type="button"
          onClick={() => fileInputRef.current.click()}
        >
          Upload Photo / Take Picture
        </button>

        <div style={{ margin: '1em 0' }}>
          <input
            type="text"
            placeholder="Location"
            value={location}
            readOnly
            required
          />
        </div>
        <div style={{ margin: '1em 0' }}>
          <input
            type="text"
            placeholder="Status"
            value={status}
            onChange={e => setStatus(e.target.value)}
            required
          />
        </div>
        {preview && (
          <div className="preview">
            <img src={preview} alt="Preview" width={250} />
          </div>
        )}
        <button type="submit" disabled={!selectedImage || loading}>
          {loading ? 'Analyzing...' : 'Check for Pothole'}
        </button>
      </form>
      {result && <div className="result">{result}</div>}
    </div>
  );
}

export default App;
