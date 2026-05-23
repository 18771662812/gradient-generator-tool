import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const setAuth = (authData) => {
    token.value = authData.token
    user.value = authData.user
    localStorage.setItem('token', authData.token)
  }

  const clearAuth = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  const checkAuth = async () => {
    if (!token.value) return

    try {
      const response = await api.auth.me()
      user.value = response.data.user
    } catch (error) {
      clearAuth()
    }
  }

  const login = async (username, password) => {
    const response = await api.auth.login({ username, password })
    setAuth(response.data)
    return response.data
  }

  const register = async (username, password) => {
    const response = await api.auth.register({ username, password })
    setAuth(response.data)
    return response.data
  }

  const logout = () => {
    clearAuth()
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth
  }
})
