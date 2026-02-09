package com.tableorder.dto.order;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderResponse {
    private Long id;
    private String orderNumber;
    private Long tableId;
    private String sessionId;
    private String status;
    private Integer totalAmount;
    private List<OrderItemResponse> items;
    private LocalDateTime createdAt;
}
