package com.tableorder.dto.order;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.util.List;

/**
 * 주문 생성 요청 DTO
 */
@Data
public class CreateOrderRequest {
    
    @NotNull(message = "매장 ID는 필수입니다")
    private Long storeId;
    
    @NotNull(message = "테이블 ID는 필수입니다")
    private Long tableId;
    
    @NotBlank(message = "세션 ID는 필수입니다")
    private String sessionId;
    
    @NotEmpty(message = "주문 항목은 최소 1개 이상이어야 합니다")
    @Valid
    private List<OrderItemRequest> items;
}
