import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOrderStore } from '@/stores/useOrderStore';
import { getSessionId } from '@/utils/storage';

const statusLabels: Record<string, string> = {
  PENDING: '대기중',
  CONFIRMED: '확인됨',
  PREPARING: '준비중',
  READY: '준비완료',
  SERVED: '서빙완료',
  COMPLETED: '완료',
  CANCELLED: '취소됨',
};

export function OrderHistoryPage() {
  const navigate = useNavigate();
  const { orders, isLoading, error, fetchOrders } = useOrderStore();

  useEffect(() => {
    fetchOrders(getSessionId());
  }, [fetchOrders]);

  if (isLoading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>주문 내역을 불러오는 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
        <p>{error}</p>
        <button onClick={() => fetchOrders(getSessionId())}>다시 시도</button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>주문 내역</h1>
        <button
          onClick={() => navigate('/')}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          메뉴로 돌아가기
        </button>
      </div>

      {orders.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <p>주문 내역이 없습니다</p>
          <button
            onClick={() => navigate('/')}
            style={{
              marginTop: '20px',
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
            }}
          >
            메뉴 보러가기
          </button>
        </div>
      ) : (
        <div>
          {orders.map((order) => (
            <div
              key={order.id}
              style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '20px',
                marginBottom: '15px',
                backgroundColor: 'white',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <h3 style={{ margin: 0 }}>주문번호: {order.orderNumber}</h3>
                <span
                  style={{
                    padding: '5px 15px',
                    backgroundColor: order.status === 'COMPLETED' ? '#28a745' : '#007bff',
                    color: 'white',
                    borderRadius: '20px',
                    fontSize: '14px',
                  }}
                >
                  {statusLabels[order.status] || order.status}
                </span>
              </div>

              <div style={{ marginTop: '15px' }}>
                <h4 style={{ margin: '0 0 10px 0', color: '#666' }}>주문 항목</h4>
                {order.items.map((item, index) => (
                  <div
                    key={index}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      padding: '8px 0',
                      borderBottom: index < order.items.length - 1 ? '1px solid #eee' : 'none',
                    }}
                  >
                    <span>
                      {item.menuName} x {item.quantity}
                    </span>
                    <span>{(item.price * item.quantity).toLocaleString()}원</span>
                  </div>
                ))}
              </div>

              <div
                style={{
                  marginTop: '15px',
                  paddingTop: '15px',
                  borderTop: '2px solid #ddd',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <span style={{ color: '#666' }}>
                  {new Date(order.createdAt).toLocaleString('ko-KR')}
                </span>
                <span style={{ fontSize: '18px', fontWeight: 'bold', color: '#007bff' }}>
                  총액: {order.totalAmount.toLocaleString()}원
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
