import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to automatically attach the token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth Services
export const login = async (data) => {
  const response = await api.post('/auth/login', data);
  return response.data;
};

export const register = async (data) => {
  const response = await api.post('/auth/register', data);
  return response.data;
};

export const getMe = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// Property Services
export const getProperties = async (params) => {
  const response = await api.get('/properties/', { params });
  return response.data;
};

export const getPropertyById = async (id) => {
  const response = await api.get(`/properties/${id}`);
  return response.data;
};

// Application Services
export const applyForProperty = async (data) => {
  const response = await api.post('/applications/', data);
  return response.data;
};

export const getApplications = async (property_id) => {
  const params = property_id ? { property_id } : {};
  const response = await api.get('/applications/', { params });
  return response.data;
};

export const updateApplicationStatus = async (id, status) => {
  const response = await api.patch(`/applications/${id}/status`, { status });
  return response.data;
};

// Appointment Services
export const bookAppointment = async (data) => {
  const response = await api.post('/appointments/', data);
  return response.data;
};

export default api;
