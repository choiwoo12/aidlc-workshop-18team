import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMenuStore } from '@/stores/useMenuStore';
import { useCartStore } from '@/stores/useCartStore';

export function MenuPage() {
  const navigate = useNavigate();
  const { menus, isLoading, error, fetchMenus } = useMenuStore();
  const { addItem, getTotalItems } = useCartStore();

  useEffect(() => {
    fetchMenus(1); // storeId = 1
  }, [fetchMenus]);

  const handleAddToCart = (menu: any) => {
    addItem(menu, 1);
    alert('장바구니에 담았습니다');
  };

  if (isLoading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>메뉴를 불러오는 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
        <p>{error}</p>
        <button onClick={() => fetchMenus(1)}>다시 시도</button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>메뉴</h1>
        <button
          onClick={() => navigate('/cart')}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          장바구니 ({getTotalItems()})
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '20px' }}>
        {menus.map((menu) => (
          <div
            key={menu.id}
            style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '15px',
              backgroundColor: 'white',
            }}
          >
            <h3 style={{ margin: '0 0 10px 0' }}>{menu.name}</h3>
            <p style={{ fontSize: '18px', fontWeight: 'bold', color: '#333', margin: '10px 0' }}>
              {menu.price.toLocaleString()}원
            </p>
            <button
              onClick={() => handleAddToCart(menu)}
              style={{
                width: '100%',
                padding: '10px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
              }}
            >
              담기
            </button>
          </div>
        ))}
      </div>

      {menus.length === 0 && (
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <p>등록된 메뉴가 없습니다</p>
        </div>
      )}
    </div>
  );
}
