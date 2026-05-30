import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'https://scoff-rants-hazelnut.ngrok-free.dev'
});

export default apiClient;


// http://localhost:8000 