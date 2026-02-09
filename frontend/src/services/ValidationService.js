/**
 * Validation Service - Unit 2: Customer Order Domain
 * 
 * 클라이언트 측 데이터 유효성 검증 서비스
 */

class ValidationService {
  /**
   * 필수 옵션 검증
   * @param {Object} menu - 메뉴 정보
   * @param {Array} selectedOptions - 선택된 옵션
   * @returns {Object} { valid: boolean, errors: string[] }
   */
  validateRequiredOptions(menu, selectedOptions) {
    const errors = [];

    if (!menu.options || !menu.options.option_groups) {
      return { valid: true, errors: [] };
    }

    menu.options.option_groups.forEach(group => {
      if (group.required) {
        const hasSelection = selectedOptions.some(
          opt => opt.group_id === group.id
        );
        if (!hasSelection) {
          errors.push(`${group.name}을(를) 선택해주세요.`);
        }
      }
    });

    return { valid: errors.length === 0, errors };
  }

  /**
   * 장바구니 검증
   * @param {Object} cart - 장바구니 데이터
   * @returns {Object} { valid: boolean, errors: string[] }
   */
  validateCart(cart) {
    if (!cart || !cart.items || cart.items.length === 0) {
      return { 
        valid: false, 
        errors: ['장바구니가 비어있습니다.'] 
      };
    }
    return { valid: true, errors: [] };
  }

  /**
   * 수량 검증
   * @param {number} quantity - 수량
   * @returns {Object} { valid: boolean, errors: string[] }
   */
  validateQuantity(quantity) {
    if (quantity < 1) {
      return { 
        valid: false, 
        errors: ['수량은 1 이상이어야 합니다.'] 
      };
    }
    return { valid: true, errors: [] };
  }

  /**
   * 사용자명 검증
   * @param {string} username
   * @returns {string|null} 에러 메시지 또는 null
   */
  validateUsername(username) {
    if (!username || username.trim() === '') {
      return '아이디를 입력해주세요.'
    }
    return null
  }

  /**
   * 비밀번호 검증
   * @param {string} password
   * @returns {string|null} 에러 메시지 또는 null
   */
  validatePassword(password) {
    if (!password || password.trim() === '') {
      return '비밀번호를 입력해주세요.'
    }
    return null
  }

  /**
   * 테이블 번호 검증
   * @param {string} tableNumber
   * @returns {string|null} 에러 메시지 또는 null
   */
  validateTableNumber(tableNumber) {
    if (!tableNumber || tableNumber.trim() === '') {
      return '테이블 번호를 입력해주세요.'
    }
    return null
  }

  /**
   * 단일/다중 선택 검증
   * @param {Object} optionGroup - 옵션 그룹
   * @param {Array} selectedOptions - 선택된 옵션 (해당 그룹)
   * @returns {Object} { valid: boolean, errors: string[] }
   */
  validateMultipleSelection(optionGroup, selectedOptions) {
    if (!optionGroup.allow_multiple && selectedOptions.length > 1) {
      return {
        valid: false,
        errors: [`${optionGroup.name}은(는) 하나만 선택 가능합니다.`]
      };
    }
    return { valid: true, errors: [] };
  }
}

export default new ValidationService();
