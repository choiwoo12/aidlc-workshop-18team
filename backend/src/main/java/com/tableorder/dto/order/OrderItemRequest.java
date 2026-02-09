package com.tableorder.dto.order;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * 주문 항목 요청 DTO
 */
@Data
public class OrderItemRequest {
    
    @NotNull(message = "메뉴 ID는 필수입니다")
    private Long menuId;
    
    @Min(value = 1, message = "수량은 1개 이상이어야 합니다")
    private Integer quantity;
}
