import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Input } from '../components/common/Input'
import { Button } from '../components/common/Button'
import { ErrorMessage } from '../components/common/ErrorMessage'
import ValidationService from '../services/ValidationService'

const LoginPage = () => {
  const navigate = useNavigate()
  const { adminLogin, tableLogin } = useAuth()
  
  const [loginType, setLoginType] = useState('table') // 'admin' or 'table'
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  // Admin login form
  const [adminUsername, setAdminUsername] = useState('')
  const [adminPassword, setAdminPassword] = useState('')
  const [adminUsernameError, setAdminUsernameError] = useState(null)
  const [adminPasswordError, setAdminPasswordError] = useState(null)
  
  // Table login form
  const [tableNumber, setTableNumber] = useState('')
  const [tableNumberError, setTableNumberError] = useState(null)
  
  const handleAdminLogin = async (e) => {
    e.preventDefault()
    setError(null)
    
    // Validate inputs
    const usernameError = ValidationService.validateUsername(adminUsername)
    const passwordError = ValidationService.validatePassword(adminPassword)
    
    setAdminUsernameError(usernameError)
    setAdminPasswordError(passwordError)
    
    if (usernameError || passwordError) {
      return
    }
    
    setLoading(true)
    
    try {
      const result = await adminLogin(adminUsername, adminPassword)
      
      if (result.success) {
        navigate('/admin/dashboard')
      } else {
        setError(result.error)
      }
    } catch (err) {
      setError('로그인 중 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }
  
  const handleTableLogin = async (e) => {
    e.preventDefault()
    setError(null)
    
    // Validate input
    const tableError = ValidationService.validateTableNumber(tableNumber)
    setTableNumberError(tableError)
    
    if (tableError) {
      return
    }
    
    setLoading(true)
    
    try {
      // For MVP, use store_id = 1 (default store)
      const result = await tableLogin(1, tableNumber)
      
      if (result.success) {
        navigate('/customer/menu')
      } else {
        setError(result.error)
      }
    } catch (err) {
      setError('로그인 중 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          테이블오더 서비스
        </h1>
        
        {/* Login type tabs */}
        <div className="flex mb-6 border-b border-gray-200">
          <button
            onClick={() => setLoginType('table')}
            className={`flex-1 py-3 text-center font-medium transition-colors ${
              loginType === 'table'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            고객 로그인
          </button>
          <button
            onClick={() => setLoginType('admin')}
            className={`flex-1 py-3 text-center font-medium transition-colors ${
              loginType === 'admin'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            관리자 로그인
          </button>
        </div>
        
        <ErrorMessage message={error} onClose={() => setError(null)} />
        
        {/* Table login form */}
        {loginType === 'table' && (
          <form onSubmit={handleTableLogin}>
            <Input
              type="text"
              label="테이블 번호"
              value={tableNumber}
              onChange={(e) => setTableNumber(e.target.value)}
              placeholder="테이블 번호를 입력하세요"
              error={tableNumberError}
              required
            />
            
            <Button
              type="submit"
              fullWidth
              disabled={loading}
            >
              {loading ? '로그인 중...' : '로그인'}
            </Button>
            
            <p className="mt-4 text-sm text-gray-600 text-center">
              테이블에 부착된 번호를 입력해주세요
            </p>
          </form>
        )}
        
        {/* Admin login form */}
        {loginType === 'admin' && (
          <form onSubmit={handleAdminLogin}>
            <Input
              type="text"
              label="아이디"
              value={adminUsername}
              onChange={(e) => setAdminUsername(e.target.value)}
              placeholder="아이디를 입력하세요"
              error={adminUsernameError}
              required
            />
            
            <Input
              type="password"
              label="비밀번호"
              value={adminPassword}
              onChange={(e) => setAdminPassword(e.target.value)}
              placeholder="비밀번호를 입력하세요"
              error={adminPasswordError}
              required
            />
            
            <Button
              type="submit"
              fullWidth
              disabled={loading}
            >
              {loading ? '로그인 중...' : '로그인'}
            </Button>
          </form>
        )}
      </div>
    </div>
  )
}

export default LoginPage
