package com.tableorder.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Order Entity
 * 주문 정보를 관리하는 도메인 엔티티
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Order {
    
    private Long id;
    private String orderNumber;
    private Long storeId;
    private Long tableId;
    private String sessionId;
    private LocalDateTime orderTime;
    private Integer totalAmount;
    private String status; // '대기중', '준비중', '완료', '취소'
    private Integer version; // 낙관적 잠금용
    private Boolean deleted;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    // 연관 관계 (조회 시 사용)
    private List<OrderItem> items;
}
