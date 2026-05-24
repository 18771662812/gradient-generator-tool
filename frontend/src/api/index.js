import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

const api = {
  auth: {
    register: (data) => apiClient.post('/auth/register', data),
    login: (data) => apiClient.post('/auth/login', data),
    me: () => apiClient.get('/auth/me')
  },
  
  gradients: {
    getMy: () => apiClient.get('/gradients/my'),
    getById: (id) => apiClient.get(`/gradients/${id}`),
    create: (data) => apiClient.post('/gradients', data),
    update: (id, data) => apiClient.put(`/gradients/${id}`, data),
    delete: (id) => apiClient.delete(`/gradients/${id}`)
  },
  
  plaza: {
    getAll: () => apiClient.get('/plaza')
  },
  
  favorites: {
    getAll: () => apiClient.get('/favorites'),
    add: (gradientId) => apiClient.post(`/favorites/${gradientId}`),
    remove: (gradientId) => apiClient.delete(`/favorites/${gradientId}`)
  }
}

export const recommendGradients = (color) =>
  apiClient.post('/gradients/recommend', { color })

export default api
