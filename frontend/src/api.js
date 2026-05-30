import axios from 'axios';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL,
    headers: {
        "ngrok-skip-browser-warning": "true"
    }
});

export default apiClient;


// http://localhost:8000 