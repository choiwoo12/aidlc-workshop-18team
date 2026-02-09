/**
 * Cart Page - Unit 2: Customer Order Domain
 * 
 * 장바구니 화면
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useCart } from '../context/CartContext';
import { useOrder } from '../context/OrderContext';
import { Button } from '../components/common/Button';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { Modal } from '../components/common/Modal';

const CartPage = () => {
  const navigate = useNavigate();
  const { isTable } = useAuth();
  const { cart, updateQuantity, removeItem, clearCart } = useCart();
  const { createOrder, loading: orderLoading } = useOrder();

  const [error, setError] = useState(null);
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);

  /**
   * 수량 변경
   */
  const handleQuantityChange = (cartItemId, newQuantity) => {
    if (newQuantity < 1) return;
    updateQuantity(cartItemId, newQuantity);
  };

  /**
   * 항목 제거
   */
  const handleRemoveItem = (cartItemId) => {
    removeItem(cartItemId);
  };

  /**
   * 주문하기 확인 모달 열기
   */
  const handleOrderClick = () => {
    if (cart.items.length === 0) {
      setError('장바구니가 비어있습니다.');
      return;
    }
    setIsConfirmModalOpen(true);
  };

  /**
   * 주문 생성
   */
  const handleConfirmOrder = async () => {
    setError(null);
    setIsConfirmModalOpen(false);

    try {
      await createOrder(cart.items);
      clearCart();
      navigate('/customer/orders');
    } catch (err) {
      console.error('Failed to create order:', err);
      setError('주문 생성에 실패했습니다. 다시 시도해주세요.');
    }
  };

  /**
   * 메뉴로 돌아가기
   */
  const handleBackToMenu = () => {
    navigate('/customer/menu');
  };

  if (!isTable) {
    navigate('/');
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={handleBackToMenu}
              className="text-gray-600 hover:text-gray-800"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 className="text-2xl font-bold text-gray-800">장바구니</h1>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <ErrorMessage message={error} onClose={() => setError(null)} />

        {/* 장바구니 항목 */}
        {cart.items.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">장바구니가 비어있습니다.</p>
            <Button onClick={handleBackToMenu}>메뉴 보러가기</Button>
          </div>
        ) : (
          <div className="space-y-4">
            {/* 항목 목록 */}
            <div className="space-y-3">
              {cart.items.map((item) => (
                <div
                  key={item.id}
                  className="bg-white rounded-lg shadow-sm p-4"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-800 mb-1">
                        {item.menu_snapshot.name}
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">
                        {item.menu_snapshot.price.toLocaleString()}원
                      </p>
                      
                      {/* 선택된 옵션 */}
                      {item.selected_options.length > 0 && (
                        <div className="text-sm text-gray-600 mb-2">
                          <span className="font-medium">옵션: </span>
                          {item.selected_options.map((opt, idx) => (
                            <span key={idx}>
                              {opt.name} (+{opt.price.toLocaleString()}원)
                              {idx < item.selected_options.length - 1 && ', '}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* 제거 버튼 */}
                    <button
                      onClick={() => handleRemoveItem(item.id)}
                      className="text-red-500 hover:text-red-700 ml-4"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>

                  {/* 수량 조절 및 소계 */}
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                        className="w-8 h-8 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors"
                      >
                        -
                      </button>
                      <span className="text-lg font-semibold w-8 text-center">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                        className="w-8 h-8 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors"
                      >
                        +
                      </button>
                    </div>
                    <span className="text-lg font-bold text-blue-600">
                      {item.subtotal.toLocaleString()}원
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {/* 총 금액 및 주문 버튼 */}
            <div className="bg-white rounded-lg shadow-sm p-6 sticky bottom-0">
              <div className="flex justify-between items-center mb-4">
                <span className="text-lg text-gray-700">총 금액</span>
                <span className="text-2xl font-bold text-blue-600">
                  {cart.total_amount.toLocaleString()}원
                </span>
              </div>
              <div className="flex gap-3">
                <Button
                  onClick={clearCart}
                  variant="secondary"
                  className="flex-1"
                >
                  전체 삭제
                </Button>
                <Button
                  onClick={handleOrderClick}
                  disabled={orderLoading}
                  className="flex-1"
                >
                  {orderLoading ? '주문 중...' : '주문하기'}
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 주문 확인 모달 */}
      <Modal
        isOpen={isConfirmModalOpen}
        onClose={() => setIsConfirmModalOpen(false)}
        title="주문 확인"
      >
        <div className="space-y-4">
          <p className="text-gray-700">
            총 <span className="font-bold">{cart.items.length}</span>개 항목,{' '}
            <span className="font-bold text-blue-600">
              {cart.total_amount.toLocaleString()}원
            </span>을 주문하시겠습니까?
          </p>
          <div className="flex gap-3">
            <Button
              onClick={() => setIsConfirmModalOpen(false)}
              variant="secondary"
              fullWidth
            >
              취소
            </Button>
            <Button
              onClick={handleConfirmOrder}
              disabled={orderLoading}
              fullWidth
            >
              {orderLoading ? '주문 중...' : '확인'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default CartPage;
