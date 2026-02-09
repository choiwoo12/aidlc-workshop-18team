package com.tableorder.dto.order;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderItemResponse {
    private Long id;
    private Long menuId;
    private String menuName;
    private Integer quantity;
    private Integer unitPrice;
    private Integer subtotal;
}
