import { createContext, useContext, useState, useEffect } from 'react'
import { StorageService } from '../services/StorageService'
import { AuthService } from '../services/AuthService'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in
    const token = StorageService.getToken()
    const userType = StorageService.getUserType()
    
    if (token && userType) {
      setUser({ userType })
    }
    
    setLoading(false)
  }, [])

  const adminLogin = async (username, password) => {
    try {
      const response = await AuthService.adminLogin(username, password)
      
      // Store token (persistent for admin)
      StorageService.setToken(response.access_token, true)
      StorageService.setUserType('admin', true)
      
      setUser({ userType: 'admin', storeId: response.store_id })
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  const tableLogin = async (storeId, tableNumber) => {
    try {
      const response = await AuthService.tableLogin(storeId, tableNumber)
      
      // Store token (session for table)
      StorageService.setToken(response.access_token, false)
      StorageService.setUserType('table', false)
      
      setUser({ userType: 'table', tableId: response.table_id })
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  const logout = () => {
    StorageService.clearAll()
    setUser(null)
  }

  const value = {
    user,
    loading,
    adminLogin,
    tableLogin,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.userType === 'admin',
    isTable: user?.userType === 'table',
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
