import axios from '../utils/axios'

/**
 * Authentication Service
 */
export const AuthService = {
  /**
   * Admin login
   */
  async adminLogin(username, password) {
    const response = await axios.post('/api/auth/admin/login', {
      username,
      password,
    })
    return response.data
  },

  /**
   * Table login
   */
  async tableLogin(storeId, tableNumber) {
    const response = await axios.post('/api/auth/table/login', {
      store_id: storeId,
      table_number: tableNumber,
    })
    return response.data
  },
}
