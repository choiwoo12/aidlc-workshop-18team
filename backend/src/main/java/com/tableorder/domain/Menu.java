package com.tableorder.domain;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Menu {
    private Long id;
    private Long storeId;
    private String name;
    private Integer price;
    private String imageUrl;
    private boolean deleted;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
