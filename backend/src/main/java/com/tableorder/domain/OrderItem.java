package com.tableorder.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * OrderItem Entity
 * 주문 항목 정보 (주문 시점 가격 스냅샷 포함)
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderItem {
    
    private Long id;
    private Long orderId;
    private Long menuId;
    private String menuName; // 스냅샷
    private Integer quantity;
    private Integer unitPrice; // 주문 시점 가격 (불변)
    private LocalDateTime createdAt;
}
