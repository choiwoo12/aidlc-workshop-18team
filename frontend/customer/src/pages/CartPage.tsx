import { useNavigate } from 'react-router-dom';
import { useCartStore } from '@/stores/useCartStore';
import { useOrderStore } from '@/stores/useOrderStore';
import { getSessionId } from '@/utils/storage';

export function CartPage() {
  const navigate = useNavigate();
  const { items, getTotalAmount, clearCart, removeItem, updateQuantity } = useCartStore();
  const { createOrder, isLoading } = useOrderStore();

  const handleCheckout = async () => {
    if (items.length === 0) {
      alert('장바구니가 비어있습니다');
      return;
    }

    try {
      await createOrder({
        storeId: 1,
        tableId: 1,
        sessionId: getSessionId(),
        items: items.map((item) => ({
          menuId: item.menuId,
          quantity: item.quantity,
        })),
      });

      clearCart();
      alert('주문이 완료되었습니다');
      navigate('/orders');
    } catch (error) {
      alert('주문 생성에 실패했습니다');
    }
  };

  if (items.length === 0) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h1>장바구니</h1>
        <div style={{ marginTop: '40px' }}>
          <p style={{ color: '#666', marginBottom: '20px' }}>장바구니가 비어있습니다</p>
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
            메뉴 보러가기
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>장바구니</h1>

      <div style={{ marginTop: '20px' }}>
        {items.map((item) => (
          <div
            key={item.menuId}
            style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '15px',
              marginBottom: '10px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              backgroundColor: 'white',
            }}
          >
            <div>
              <h3 style={{ margin: '0 0 5px 0' }}>{item.menuName}</h3>
              <p style={{ margin: '0', color: '#666' }}>
                {item.price.toLocaleString()}원 x {item.quantity}개
              </p>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <button
                onClick={() => updateQuantity(item.menuId, item.quantity - 1)}
                style={{
                  padding: '5px 10px',
                  backgroundColor: '#6c757d',
                  color: 'white',
                  border: 'none',
                  borderRadius: '3px',
                  cursor: 'pointer',
                }}
              >
                -
              </button>
              <span style={{ minWidth: '30px', textAlign: 'center' }}>{item.quantity}</span>
              <button
                onClick={() => updateQuantity(item.menuId, item.quantity + 1)}
                style={{
                  padding: '5px 10px',
                  backgroundColor: '#6c757d',
                  color: 'white',
                  border: 'none',
                  borderRadius: '3px',
                  cursor: 'pointer',
                }}
              >
                +
              </button>
              <button
                onClick={() => removeItem(item.menuId)}
                style={{
                  padding: '5px 15px',
                  backgroundColor: '#dc3545',
                  color: 'white',
                  border: 'none',
                  borderRadius: '3px',
                  cursor: 'pointer',
                  marginLeft: '10px',
                }}
              >
                삭제
              </button>
            </div>
          </div>
        ))}
      </div>

      <div
        style={{
          marginTop: '30px',
          padding: '20px',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
          <h2 style={{ margin: 0 }}>총액</h2>
          <h2 style={{ margin: 0, color: '#007bff' }}>{getTotalAmount().toLocaleString()}원</h2>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => navigate('/')}
            style={{
              flex: 1,
              padding: '15px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '16px',
            }}
          >
            계속 쇼핑
          </button>
          <button
            onClick={handleCheckout}
            disabled={isLoading}
            style={{
              flex: 1,
              padding: '15px',
              backgroundColor: isLoading ? '#ccc' : '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              fontSize: '16px',
            }}
          >
            {isLoading ? '주문 중...' : '주문하기'}
          </button>
        </div>
      </div>
    </div>
  );
}
