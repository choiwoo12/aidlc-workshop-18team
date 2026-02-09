/**
 * Storage Service
 * Manages LocalStorage and SessionStorage
 */

const TOKEN_KEY = 'auth_token'
const USER_TYPE_KEY = 'user_type'

export const StorageService = {
  // Token management
  getToken() {
    return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY)
  },

  setToken(token, persistent = false) {
    if (persistent) {
      localStorage.setItem(TOKEN_KEY, token)
    } else {
      sessionStorage.setItem(TOKEN_KEY, token)
    }
  },

  clearToken() {
    localStorage.removeItem(TOKEN_KEY)
    sessionStorage.removeItem(TOKEN_KEY)
  },

  // User type management
  getUserType() {
    return localStorage.getItem(USER_TYPE_KEY) || sessionStorage.getItem(USER_TYPE_KEY)
  },

  setUserType(userType, persistent = false) {
    if (persistent) {
      localStorage.setItem(USER_TYPE_KEY, userType)
    } else {
      sessionStorage.setItem(USER_TYPE_KEY, userType)
    }
  },

  clearUserType() {
    localStorage.removeItem(USER_TYPE_KEY)
    sessionStorage.removeItem(USER_TYPE_KEY)
  },

  // Clear all
  clearAll() {
    this.clearToken()
    this.clearUserType()
  },
}
