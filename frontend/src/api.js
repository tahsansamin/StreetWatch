import axios from 'axios';

const apiClient = axios.create({
    baseURL: "https://scoff-rants-hazelnut.ngrok-free.dev",
    headers: {
        "ngrok-skip-browser-warning": "true"
    }
});

export default apiClient;


// http://localhost:8000 