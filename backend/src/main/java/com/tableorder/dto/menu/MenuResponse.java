package com.tableorder.dto.menu;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MenuResponse {
    private Long id;
    private Long storeId;
    private String name;
    private Integer price;
    private String imageUrl;
    private LocalDateTime createdAt;
}
