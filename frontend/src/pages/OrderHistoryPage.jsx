/**
 * Order History Page - Unit 2: Customer Order Domain
 * 
 * 주문 내역 화면 (실시간 업데이트)
 */

import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useOrder } from '../context/OrderContext';
import { Button } from '../components/common/Button';
import { Loading } from '../components/common/Loading';
import { ErrorMessage } from '../components/common/ErrorMessage';

const OrderHistoryPage = () => {
  const navigate = useNavigate();
  const { isTable } = useAuth();
  const { orders, loading, error, sseConnected, refreshOrders } = useOrder();

  /**
   * 주문 상태 표시 텍스트
   */
  const getStatusText = (status) => {
    const statusMap = {
      'PENDING': '접수 대기',
      'CONFIRMED': '접수 완료',
      'PREPARING': '조리 중',
      'READY': '준비 완료',
      'SERVED': '서빙 완료',
      'CANCELLED': '취소됨'
    };
    return statusMap[status] || status;
  };

  /**
   * 주문 상태 색상
   */
  const getStatusColor = (status) => {
    const colorMap = {
      'PENDING': 'bg-yellow-100 text-yellow-800',
      'CONFIRMED': 'bg-blue-100 text-blue-800',
      'PREPARING': 'bg-purple-100 text-purple-800',
      'READY': 'bg-green-100 text-green-800',
      'SERVED': 'bg-gray-100 text-gray-800',
      'CANCELLED': 'bg-red-100 text-red-800'
    };
    return colorMap[status] || 'bg-gray-100 text-gray-800';
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

  if (loading && orders.length === 0) {
    return <Loading message="주문 내역을 불러오는 중..." />;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={handleBackToMenu}
                className="text-gray-600 hover:text-gray-800"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <h1 className="text-2xl font-bold text-gray-800">주문 내역</h1>
            </div>

            {/* SSE 연결 상태 표시 */}
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${sseConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-gray-600">
                {sseConnected ? '실시간 연결' : '연결 끊김'}
              </span>
              {!sseConnected && (
                <button
                  onClick={refreshOrders}
                  className="ml-2 text-blue-600 hover:text-blue-800 text-sm"
                >
                  새로고침
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <ErrorMessage message={error} onClose={() => {}} />

        {/* 주문 내역 */}
        {orders.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">주문 내역이 없습니다.</p>
            <Button onClick={handleBackToMenu}>메뉴 보러가기</Button>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => (
              <div
                key={order.id}
                className="bg-white rounded-lg shadow-sm p-4"
              >
                {/* 주문 헤더 */}
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">
                      주문번호: {order.order_number}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {new Date(order.created_at).toLocaleString('ko-KR')}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                    {getStatusText(order.status)}
                  </span>
                </div>

                {/* 주문 항목 */}
                <div className="space-y-2 mb-4">
                  {order.items && order.items.map((item, idx) => (
                    <div key={idx} className="flex justify-between text-sm">
                      <div className="flex-1">
                        <span className="text-gray-800">{item.menu_name_snapshot}</span>
                        {item.selected_options && item.selected_options.length > 0 && (
                          <span className="text-gray-600 ml-2">
                            ({item.selected_options.map(opt => opt.name).join(', ')})
                          </span>
                        )}
                        <span className="text-gray-600 ml-2">x {item.quantity}</span>
                      </div>
                      <span className="text-gray-800">
                        {item.subtotal.toLocaleString()}원
                      </span>
                    </div>
                  ))}
                </div>

                {/* 총 금액 */}
                <div className="border-t pt-3 flex justify-between items-center">
                  <span className="text-gray-700 font-medium">총 금액</span>
                  <span className="text-xl font-bold text-blue-600">
                    {order.total_amount.toLocaleString()}원
                  </span>
                </div>

                {/* 주문 상태별 안내 메시지 */}
                {order.status === 'READY' && (
                  <div className="mt-3 bg-green-50 border border-green-200 rounded-lg p-3">
                    <p className="text-sm text-green-800">
                      🎉 주문하신 음식이 준비되었습니다!
                    </p>
                  </div>
                )}
                {order.status === 'PREPARING' && (
                  <div className="mt-3 bg-purple-50 border border-purple-200 rounded-lg p-3">
                    <p className="text-sm text-purple-800">
                      👨‍🍳 주문하신 음식을 조리 중입니다.
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default OrderHistoryPage;
