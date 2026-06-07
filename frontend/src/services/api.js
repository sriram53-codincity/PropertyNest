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

export const getAdminUsers = async () => {
  const response = await api.get('/auth/users');
  return response.data;
};

export const deleteAdminUser = async (userId) => {
  const response = await api.delete(`/auth/users/${userId}`);
  return response.data;
};

// Property Services
export const getProperties = async (params) => {
  const response = await api.get('/properties/', { params });
  return response.data;
};

export const getMyProperties = async () => {
  const response = await api.get('/properties/mine');
  return response.data;
};

export const getAdminProperties = async () => {
  const response = await api.get('/properties/admin/all');
  return response.data;
};

export const getPropertyById = async (id) => {
  const response = await api.get(`/properties/${id}`);
  return response.data;
};

export const createProperty = async (data) => {
  const response = await api.post('/properties/', data);
  return response.data;
};

export const updateProperty = async (id, data) => {
  const response = await api.patch(`/properties/${id}`, data);
  return response.data;
};

export const deleteProperty = async (id) => {
  const response = await api.delete(`/properties/${id}`);
  return response.data;
};

export const uploadPropertyImages = async (id, formData) => {
  const response = await api.post(`/properties/${id}/images`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
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

export const updateApplicationStatus = async (id, status, reason = null) => {
  const payload = { status };
  if (reason) payload.reason = reason;
  const response = await api.patch(`/applications/${id}/status`, payload);
  return response.data;
};

export const uploadApplicationDocument = async (id, formData) => {
  const response = await api.post(`/applications/${id}/document`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const getApplicationById = async (id) => {
  const response = await api.get(`/applications/${id}`);
  return response.data;
};

export const deleteApplication = async (id) => {
  const response = await api.delete(`/applications/${id}`);
  return response.data;
};

// Appointment Services
export const bookAppointment = async (data) => {
  const response = await api.post('/appointments/', data);
  return response.data;
};

export const getMyAppointments = async () => {
  const response = await api.get('/appointments/mine');
  return response.data;
};

export const getOwnerAppointments = async () => {
  const response = await api.get('/appointments/for-owner');
  return response.data;
};

export const getAppointments = async () => {
  const response = await api.get('/appointments/');
  return response.data;
};

export const updateAppointmentStatus = async (id, status) => {
  const response = await api.patch(`/appointments/${id}/status`, { status });
  return response.data;
};

export const deleteAppointment = async (id) => {
  const response = await api.delete(`/appointments/${id}`);
  return response.data;
};

// Seller Request Services
export const createSellerRequest = async (formData) => {
  // We use the raw api instance because formData needs multipart/form-data headers.
  // Axios will automatically set the correct content-type boundary if we pass FormData.
  const response = await api.post('/seller-requests/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const getAllSellerRequests = async (status = null) => {
  const params = status ? { status } : {};
  const response = await api.get('/seller-requests/', { params });
  return response.data;
};

export const updateSellerRequestStatus = async (id, status) => {
  const response = await api.patch(`/seller-requests/${id}/status`, { status });
  return response.data;
};

export const getMySellerRequests = async () => {
  const response = await api.get('/seller-requests/mine');
  return response.data;
};

export const deleteSellerRequest = async (id) => {
  const response = await api.delete(`/seller-requests/${id}`);
  return response.data;
};

// Lease Services
export const createLease = async (data) => {
  const response = await api.post('/leases/', data);
  return response.data;
};

export const getMyLeases = async () => {
  const response = await api.get('/leases/me');
  return response.data;
};

export const getLeaseById = async (id) => {
  const response = await api.get(`/leases/${id}`);
  return response.data;
};

// Maintenance Services
export const createMaintenanceRequest = async (data) => {
  const response = await api.post('/maintenance/', data);
  return response.data;
};

export const getMaintenanceRequests = async () => {
  const response = await api.get('/maintenance/');
  return response.data;
};

export const getMaintenanceRequestById = async (id) => {
  const response = await api.get(`/maintenance/${id}`);
  return response.data;
};

export const updateMaintenanceRequestStatus = async (id, status, comment = null) => {
  const payload = { status };
  if (comment) payload.comment = comment;
  const response = await api.patch(`/maintenance/${id}/status`, payload);
  return response.data;
};

export const uploadMaintenanceImages = async (id, formData) => {
  const response = await api.post(`/maintenance/${id}/images`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const deleteMaintenanceRequest = async (id) => {
  const response = await api.delete(`/maintenance/${id}`);
  return response.data;
};

export default api;
