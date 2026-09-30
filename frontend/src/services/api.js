import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
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

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getCurrentUser: () => api.get('/api/auth/me'),
};

export const documentsAPI = {
  upload: (formData) => api.post('/api/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getAll: (params) => api.get('/api/documents', { params }),
  getById: (id) => api.get(`/api/documents/${id}`),
  delete: (id) => api.delete(`/api/documents/${id}`),
};

export const comparisonsAPI = {
  create: (data) => api.post('/api/comparisons', data),
  getAll: (params) => api.get('/api/comparisons', { params }),
  getById: (id) => api.get(`/api/comparisons/${id}`),
  delete: (id) => api.delete(`/api/comparisons/${id}`),
};

export const reportsAPI = {
  get: (comparisonId) => api.get(`/api/reports/${comparisonId}`),
  generate: (comparisonId) => api.post(`/api/reports/${comparisonId}/generate`),
  download: (comparisonId) => api.get(`/api/reports/${comparisonId}/download`, {
    responseType: 'blob'
  }),
};

export const dashboardAPI = {
  student: () => api.get('/api/dashboard/student'),
  faculty: () => api.get('/api/dashboard/faculty'),
  admin: () => api.get('/api/dashboard/admin'),
};

export default api;
