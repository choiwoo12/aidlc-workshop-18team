package com.tableorder.domain;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Table {
    private Long id;
    private Long storeId;
    private Integer tableNumber;
    private String sessionId;
    private boolean sessionActive;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
