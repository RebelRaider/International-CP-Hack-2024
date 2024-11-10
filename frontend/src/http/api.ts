import axios from 'axios';

export const API_URL = "https://91.224.87.165.sslip.io/api/v1"

const api = axios.create({
    withCredentials: true,
    baseURL: API_URL,
})

api.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    return config;
})

export default api;