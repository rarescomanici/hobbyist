import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User endpoints
export const getUsers = async (email) => {
  const response = await api.get(`/users/${email}`);
  return response.data;
};

export const registerUser = async (user) => {
  const response = await api.post('/users/register', user);
  return response.data;
};

export const updateUserProfile = async (email, profile) => {
  const response = await api.post(`/users/${email}/profile`, profile);
  return response.data;
};

// Recommendation endpoints
export const getRecommendations = async (email) => {
  const response = await api.get(`/recommendations/${email}`);
  return response.data;
};

export const generateWeeklyPlan = async (email) => {
  const response = await api.post(`/recommendations/weekly-plan/${email}`);
  return response.data;
};

export const getProgress = async (email, week) => {
  const response = await api.get(`/recommendations/${email}/progress/${week}`);
  return response.data;
};

export const markCompleted = async (email, activityId) => {
  const response = await api.post(`/recommendations/complete/${email}/${activityId}`);
  return response.data;
};

// Search & Browse endpoints
export const searchHobbies = async (query) => {
  const response = await api.get(`/search/hobbies?query=${query}`);
  return response.data;
};

export const getTrending = async () => {
  const response = await api.get('/trending');
  return response.data;
};

export const getCategories = async () => {
  const response = await api.get('/categories');
  return response.data;
};

// UI Endpoints
export const getGetStartedKey = async () => {
  const response = await api.get('/ui/get-started');
  return response.data;
};

export const getInterestFormResponseKey = async () => {
  const response = await api.get('/ui/interest-form-response');
  return response.data;
};

export const getHobbyDashboardKey = async () => {
  const response = await api.get('/ui/hobby-dashboard');
  return response.data;
};

export default api;