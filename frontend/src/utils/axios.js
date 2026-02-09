import axios from 'axios'
import { StorageService } from '../services/StorageService'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add JWT token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = StorageService.getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle errors
axiosInstance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      // Server responded with error
      const { status, data } = error.response
      
      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        StorageService.clearToken()
        window.location.href = '/login'
      }
      
      // Return error message from server
      const errorMessage = data?.error?.message || '오류가 발생했습니다'
      return Promise.reject(new Error(errorMessage))
    } else if (error.request) {
      // Request made but no response
      return Promise.reject(new Error('서버에 연결할 수 없습니다'))
    } else {
      // Something else happened
      return Promise.reject(error)
    }
  }
)

export default axiosInstance
