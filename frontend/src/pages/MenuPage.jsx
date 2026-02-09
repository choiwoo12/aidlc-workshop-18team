/**
 * Menu Page - Unit 2: Customer Order Domain
 * 
 * 메뉴 목록 및 장바구니 추가 화면
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useCart } from '../context/CartContext';
import MenuService from '../services/MenuService';
import { Button } from '../components/common/Button';
import { Loading } from '../components/common/Loading';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { Modal } from '../components/common/Modal';

const MenuPage = () => {
  const navigate = useNavigate();
  const { user, isTable } = useAuth();
  const { cart, addItem, getItemCount } = useCart();

  const [menus, setMenus] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 옵션 선택 모달
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState(null);
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [quantity, setQuantity] = useState(1);

  /**
   * 메뉴 목록 조회
   */
  useEffect(() => {
    if (!isTable) {
      navigate('/');
      return;
    }

    fetchMenus();
  }, [isTable, selectedCategory]);

  const fetchMenus = async () => {
    setLoading(true);
    setError(null);

    try {
      const menuList = await MenuService.getMenus(1, selectedCategory);
      setMenus(menuList);

      // 카테고리 목록 추출 (중복 제거)
      const uniqueCategories = [...new Set(menuList.map(menu => menu.category))];
      setCategories(uniqueCategories);
    } catch (err) {
      console.error('Failed to fetch menus:', err);
      setError('메뉴를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * 메뉴 클릭 - 옵션 선택 모달 열기
   */
  const handleMenuClick = (menu) => {
    setSelectedMenu(menu);
    setSelectedOptions([]);
    setQuantity(1);
    setIsModalOpen(true);
  };

  /**
   * 옵션 선택 토글
   */
  const handleOptionToggle = (option) => {
    setSelectedOptions((prev) => {
      const exists = prev.find(opt => opt.name === option.name);
      if (exists) {
        return prev.filter(opt => opt.name !== option.name);
      } else {
        return [...prev, option];
      }
    });
  };

  /**
   * 장바구니에 추가
   */
  const handleAddToCart = () => {
    if (!selectedMenu) return;

    addItem(selectedMenu, selectedOptions, quantity);
    setIsModalOpen(false);
    setSelectedMenu(null);
    setSelectedOptions([]);
    setQuantity(1);
  };

  /**
   * 장바구니로 이동
   */
  const handleGoToCart = () => {
    navigate('/customer/cart');
  };

  if (loading) {
    return <Loading message="메뉴를 불러오는 중..." />;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-800">메뉴</h1>
            <button
              onClick={handleGoToCart}
              className="relative bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              장바구니
              {getItemCount() > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center">
                  {getItemCount()}
                </span>
              )}
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <ErrorMessage message={error} onClose={() => setError(null)} />

        {/* 카테고리 필터 */}
        <div className="mb-6 flex gap-2 overflow-x-auto pb-2">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-2 rounded-lg whitespace-nowrap transition-colors ${
              selectedCategory === null
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            전체
          </button>
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg whitespace-nowrap transition-colors ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* 메뉴 목록 */}
        {menus.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">판매 가능한 메뉴가 없습니다.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {menus.map((menu) => (
              <div
                key={menu.id}
                onClick={() => handleMenuClick(menu)}
                className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer overflow-hidden"
              >
                {menu.image_url && (
                  <img
                    src={menu.image_url}
                    alt={menu.name}
                    className="w-full h-48 object-cover"
                  />
                )}
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-800 mb-1">
                    {menu.name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-2">{menu.description}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xl font-bold text-blue-600">
                      {menu.price.toLocaleString()}원
                    </span>
                    <span className="text-sm text-gray-500">{menu.category}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 옵션 선택 모달 */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={selectedMenu?.name}
      >
        <div className="space-y-4">
          {/* 메뉴 정보 */}
          <div>
            <p className="text-gray-600 mb-2">{selectedMenu?.description}</p>
            <p className="text-xl font-bold text-blue-600">
              {selectedMenu?.price.toLocaleString()}원
            </p>
          </div>

          {/* 옵션 선택 */}
          {selectedMenu?.options && selectedMenu.options.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-800 mb-2">옵션 선택</h4>
              <div className="space-y-2">
                {selectedMenu.options.map((option, index) => (
                  <label
                    key={index}
                    className="flex items-center justify-between p-3 border rounded-lg cursor-pointer hover:bg-gray-50"
                  >
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={selectedOptions.some(opt => opt.name === option.name)}
                        onChange={() => handleOptionToggle(option)}
                        className="mr-3"
                      />
                      <span className="text-gray-800">{option.name}</span>
                    </div>
                    <span className="text-gray-600">
                      +{option.price.toLocaleString()}원
                    </span>
                  </label>
                ))}
              </div>
            </div>
          )}

          {/* 수량 선택 */}
          <div>
            <h4 className="font-semibold text-gray-800 mb-2">수량</h4>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-10 h-10 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors"
              >
                -
              </button>
              <span className="text-xl font-semibold w-12 text-center">
                {quantity}
              </span>
              <button
                onClick={() => setQuantity(quantity + 1)}
                className="w-10 h-10 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors"
              >
                +
              </button>
            </div>
          </div>

          {/* 총 금액 */}
          <div className="border-t pt-4">
            <div className="flex justify-between items-center mb-4">
              <span className="text-gray-700">총 금액</span>
              <span className="text-2xl font-bold text-blue-600">
                {(
                  (selectedMenu?.price || 0) +
                  selectedOptions.reduce((sum, opt) => sum + opt.price, 0)
                ) * quantity}
                원
              </span>
            </div>
            <Button onClick={handleAddToCart} fullWidth>
              장바구니에 추가
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default MenuPage;
