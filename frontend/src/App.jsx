import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { CartProvider } from './context/CartContext'
import { OrderProvider } from './context/OrderContext'
import LoginPage from './pages/LoginPage'
import MenuPage from './pages/MenuPage'
import CartPage from './pages/CartPage'
import OrderHistoryPage from './pages/OrderHistoryPage'

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <OrderProvider>
          <Router>
            <Routes>
              <Route path="/" element={<LoginPage />} />
              <Route path="/login" element={<LoginPage />} />
              
              {/* Unit 2: Customer Order Domain */}
              <Route path="/customer/menu" element={<MenuPage />} />
              <Route path="/customer/cart" element={<CartPage />} />
              <Route path="/customer/orders" element={<OrderHistoryPage />} />
              
              {/* Unit 3: Admin Operations Domain - To be added */}
            </Routes>
          </Router>
        </OrderProvider>
      </CartProvider>
    </AuthProvider>
  )
}

export default App
