# Backend Implementation Guide

## Overview
이 문서는 Backend 유닛의 나머지 구현을 위한 상세 가이드입니다. 핵심 파일들은 이미 생성되었으며, 이 가이드를 참고하여 나머지 클래스들을 구현하세요.

---

## 생성된 핵심 파일

### 1. Project Structure
- ✅ `backend/pom.xml` - Maven 프로젝트 설정
- ✅ `backend/README.md` - 프로젝트 문서

### 2. Domain Layer
- ✅ `Order.java` - 주문 엔티티
- ✅ `OrderItem.java` - 주문 항목 엔티티

### 3. DTO Layer
- ✅ `ApiResponse.java` - 통일된 API 응답
- ✅ `CreateOrderRequest.java` - 주문 생성 요청
- ✅ `OrderItemRequest.java` - 주문 항목 요청

### 4. Exception Layer
- ✅ `BusinessException.java` - 비즈니스 예외 기본 클래스
- ✅ `GlobalExceptionHandler.java` - 전역 예외 처리

### 5. Main Application
- ✅ `TableOrderApplication.java` - Spring Boot 메인 클래스

### 6. Configuration
- ✅ `application.yml` - 애플리케이션 설정

### 7. Database
- ✅ `schema.sql` - 데이터베이스 스키마
- ✅ `data.sql` - 샘플 데이터

---

## 구현해야 할 나머지 클래스

### Phase 1: Domain Entities (6개 추가)

**1.1 Store.java**
```java
package com.tableorder.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Store {
    private Long id;
    private String name;
    private String address;
    private String phone;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

**1.2 Table.java**
```java
package com.tableorder.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Table {
    private Long id;
    private Long storeId;
    private Integer tableNumber;
    private String pin; // SHA-256 hashed
    private String sessionId; // UUID
    private String sessionStatus; // 'ACTIVE', 'INACTIVE'
    private LocalDateTime sessionStartTime;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

**1.3 Menu.java**
```java
package com.tableorder.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Menu {
    private Long id;
    private Long storeId;
    private String name;
    private Integer price;
    private String description;
    private String category;
    private String imagePath;
    private Integer displayOrder;
    private Boolean deleted;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

**1.4 OrderHistory.java**
```java
package com.tableorder.domain;

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
public class OrderHistory {
    private Long id;
    private Long orderId;
    private String orderNumber;
    private Long storeId;
    private Long tableId;
    private String sessionId;
    private LocalDateTime orderTime;
    private Integer totalAmount;
    private String status;
    private LocalDateTime completedTime;
    private LocalDateTime archivedTime;
    private LocalDateTime createdAt;
    private List<OrderHistoryItem> items;
}
```

**1.5 OrderHistoryItem.java**
```java
package com.tableorder.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderHistoryItem {
    private Long id;
    private Long orderHistoryId;
    private Long menuId;
    private String menuName;
    private Integer quantity;
    private Integer unitPrice;
    private LocalDateTime createdAt;
}
```

**1.6 User.java**
```java
package com.tableorder.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id;
    private Long storeId;
    private String username;
    private String password; // bcrypt hashed
    private String role; // 'ADMIN', 'MANAGER'
    private Integer loginAttempts;
    private LocalDateTime lockedUntil;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

---

### Phase 2: DTO Classes (10개 추가)

**위치**: `backend/src/main/java/com/tableorder/dto/`

**2.1 order 패키지**
- `OrderResponse.java` - 주문 응답
- `OrderItemResponse.java` - 주문 항목 응답
- `UpdateOrderStatusRequest.java` - 주문 상태 변경 요청

**2.2 menu 패키지**
- `CreateMenuRequest.java` - 메뉴 생성 요청
- `UpdateMenuRequest.java` - 메뉴 수정 요청
- `MenuResponse.java` - 메뉴 응답

**2.3 table 패키지**
- `TableResponse.java` - 테이블 응답
- `StartSessionRequest.java` - 세션 시작 요청

**2.4 auth 패키지**
- `LoginRequest.java` - 로그인 요청
- `LoginResponse.java` - 로그인 응답
- `UserResponse.java` - 사용자 응답

**2.5 sse 패키지**
- `SseEvent.java` - SSE 이벤트

**템플릿 예시 (OrderResponse.java)**:
```java
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
    private Long storeId;
    private Long tableId;
    private String sessionId;
    private LocalDateTime orderTime;
    private Integer totalAmount;
    private String status;
    private Integer version;
    private List<OrderItemResponse> items;
    
    public static OrderResponse from(Order order) {
        return OrderResponse.builder()
                .id(order.getId())
                .orderNumber(order.getOrderNumber())
                .storeId(order.getStoreId())
                .tableId(order.getTableId())
                .sessionId(order.getSessionId())
                .orderTime(order.getOrderTime())
                .totalAmount(order.getTotalAmount())
                .status(order.getStatus())
                .version(order.getVersion())
                .items(order.getItems().stream()
                        .map(OrderItemResponse::from)
                        .collect(Collectors.toList()))
                .build();
    }
}
```

---

### Phase 3: Exception Classes (6개 추가)

**위치**: `backend/src/main/java/com/tableorder/exception/`

**템플릿**:
```java
package com.tableorder.exception;

import org.springframework.http.HttpStatus;

public class OrderNotFoundException extends BusinessException {
    public OrderNotFoundException(String message) {
        super(message, HttpStatus.NOT_FOUND, "ORDER_NOT_FOUND");
    }
}
```

**구현할 예외**:
- `OrderNotFoundException.java`
- `InvalidSessionException.java`
- `MenuNotFoundException.java`
- `InvalidStatusTransitionException.java`
- `OptimisticLockException.java`
- `AccountLockedException.java`
- `FileUploadException.java`
- `TableNotFoundException.java`

---

### Phase 4: Mapper Layer (7개 Mapper + XML)

**위치**: 
- Interface: `backend/src/main/java/com/tableorder/mapper/`
- XML: `backend/src/main/resources/mybatis/mapper/`

**4.1 OrderMapper.java 예시**:
```java
package com.tableorder.mapper;

import com.tableorder.domain.Order;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

@Mapper
public interface OrderMapper {
    void insertOrder(Order order);
    Order selectById(@Param("id") Long id);
    List<Order> selectByTableAndSession(@Param("tableId") Long tableId, 
                                        @Param("sessionId") String sessionId);
    int updateOrderStatus(@Param("id") Long id, 
                          @Param("status") String status, 
                          @Param("version") Integer version);
    void updateOrderDeleted(@Param("id") Long id);
}
```

**4.2 OrderMapper.xml 예시**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.tableorder.mapper.OrderMapper">
    
    <resultMap id="OrderResultMap" type="com.tableorder.domain.Order">
        <id property="id" column="id"/>
        <result property="orderNumber" column="order_number"/>
        <result property="storeId" column="store_id"/>
        <result property="tableId" column="table_id"/>
        <result property="sessionId" column="session_id"/>
        <result property="orderTime" column="order_time"/>
        <result property="totalAmount" column="total_amount"/>
        <result property="status" column="status"/>
        <result property="version" column="version"/>
        <result property="deleted" column="deleted"/>
        <result property="createdAt" column="created_at"/>
        <result property="updatedAt" column="updated_at"/>
    </resultMap>
    
    <insert id="insertOrder" parameterType="Order" useGeneratedKeys="true" keyProperty="id">
        INSERT INTO orders (order_number, store_id, table_id, session_id, 
                           order_time, total_amount, status, version, deleted)
        VALUES (#{orderNumber}, #{storeId}, #{tableId}, #{sessionId},
                #{orderTime}, #{totalAmount}, #{status}, #{version}, #{deleted})
    </insert>
    
    <select id="selectById" resultMap="OrderResultMap">
        SELECT * FROM orders WHERE id = #{id} AND deleted = FALSE
    </select>
    
    <select id="selectByTableAndSession" resultMap="OrderResultMap">
        SELECT * FROM orders 
        WHERE table_id = #{tableId} 
          AND session_id = #{sessionId}
          AND deleted = FALSE
        ORDER BY order_time DESC
    </select>
    
    <update id="updateOrderStatus">
        UPDATE orders 
        SET status = #{status}, 
            version = version + 1,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = #{id} AND version = #{version}
    </update>
    
    <update id="updateOrderDeleted">
        UPDATE orders 
        SET deleted = TRUE, updated_at = CURRENT_TIMESTAMP
        WHERE id = #{id}
    </update>
    
</mapper>
```

**구현할 Mapper**:
- `StoreMapper.java` + `StoreMapper.xml`
- `TableMapper.java` + `TableMapper.xml`
- `MenuMapper.java` + `MenuMapper.xml`
- `OrderMapper.java` + `OrderMapper.xml` (위 예시 참고)
- `OrderItemMapper.java` + `OrderItemMapper.xml`
- `OrderHistoryMapper.java` + `OrderHistoryMapper.xml`
- `UserMapper.java` + `UserMapper.xml`

---

### Phase 5: Utility Classes (3개)

**위치**: `backend/src/main/java/com/tableorder/util/`

**5.1 OrderNumberGenerator.java**:
```java
package com.tableorder.util;

import org.springframework.stereotype.Component;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

@Component
public class OrderNumberGenerator {
    
    private static final DateTimeFormatter DATE_FORMATTER = 
        DateTimeFormatter.ofPattern("yyyyMMdd");
    
    public String generateOrderNumber(LocalDate date, int sequence) {
        String dateStr = date.format(DATE_FORMATTER);
        String seqStr = String.format("%04d", sequence);
        return "ORD-" + dateStr + "-" + seqStr;
    }
}
```

**5.2 HashUtil.java**:
```java
package com.tableorder.util;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class HashUtil {
    
    public static String sha256(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not found", e);
        }
    }
}
```

**5.3 DateTimeUtil.java**:
```java
package com.tableorder.util;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class DateTimeUtil {
    
    public static LocalDateTime now() {
        return LocalDateTime.now();
    }
    
    public static String format(LocalDateTime dateTime, String pattern) {
        return dateTime.format(DateTimeFormatter.ofPattern(pattern));
    }
    
    public static boolean isExpired(LocalDateTime expiryTime) {
        return expiryTime != null && expiryTime.isBefore(LocalDateTime.now());
    }
}
```

---

### Phase 6: Security Layer (3개)

**위치**: `backend/src/main/java/com/tableorder/security/`

**6.1 JwtTokenProvider.java** - JWT 토큰 생성 및 검증
**6.2 JwtAuthenticationFilter.java** - JWT 인증 필터
**6.3 SecurityConfig.java** - Spring Security 설정

상세 구현은 NFR Design의 Security Patterns 참고

---

### Phase 7: Infrastructure Layer (2개)

**위치**: `backend/src/main/java/com/tableorder/infrastructure/`

**7.1 SSEService.java** - SSE 연결 관리 및 이벤트 전송
**7.2 FileService.java** - 파일 업로드/삭제

상세 구현은 NFR Design의 Infrastructure Components 참고

---

### Phase 8: Service Layer (5개)

**위치**: `backend/src/main/java/com/tableorder/service/`

**8.1 OrderService.java** - 주문 비즈니스 로직
**8.2 MenuService.java** - 메뉴 비즈니스 로직
**8.3 TableService.java** - 테이블 세션 관리
**8.4 AuthService.java** - 인증 및 로그인
**8.5 StoreService.java** - 매장 정보 조회

상세 구현은 Functional Design의 Business Logic Model 참고

---

### Phase 9: Controller Layer (8개)

**위치**: `backend/src/main/java/com/tableorder/controller/`

**Customer Controllers**:
- `CustomerOrderController.java` - 고객 주문 API
- `CustomerMenuController.java` - 고객 메뉴 조회 API
- `CustomerSSEController.java` - 고객 SSE 연결

**Admin Controllers**:
- `AdminOrderController.java` - 관리자 주문 관리 API
- `AdminMenuController.java` - 관리자 메뉴 관리 API
- `AdminTableController.java` - 관리자 테이블 관리 API
- `AdminSSEController.java` - 관리자 SSE 연결

**Auth Controller**:
- `AuthController.java` - 로그인 API

---

### Phase 10: Configuration Classes (5개)

**위치**: `backend/src/main/java/com/tableorder/config/`

**10.1 CacheConfig.java** - Caffeine 캐시 설정
**10.2 AsyncConfig.java** - 비동기 처리 설정
**10.3 RetryConfig.java** - 재시도 설정
**10.4 CorsConfig.java** - CORS 설정
**10.5 SwaggerConfig.java** - Swagger/OpenAPI 설정

상세 구현은 NFR Design의 Configuration Components 참고

---

## 구현 우선순위

1. **High Priority** (핵심 기능):
   - Domain Entities (모든 엔티티)
   - Mapper Layer (OrderMapper, MenuMapper, TableMapper)
   - Service Layer (OrderService, MenuService, TableService)
   - Controller Layer (CustomerOrderController, AdminOrderController)

2. **Medium Priority** (필수 기능):
   - Security Layer (JWT, SecurityConfig)
   - Infrastructure Layer (SSEService, FileService)
   - Configuration Layer (모든 Config)

3. **Low Priority** (부가 기능):
   - Utility Classes
   - 나머지 DTO 및 Exception

---

## 테스트 작성 가이드

각 레이어별로 단위 테스트를 작성하세요:

**Service Layer Test 예시**:
```java
@SpringBootTest
class OrderServiceTest {
    
    @Autowired
    private OrderService orderService;
    
    @MockBean
    private OrderMapper orderMapper;
    
    @Test
    void createOrder_Success() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest();
        // ... setup request
        
        // When
        OrderResponse response = orderService.createOrder(request);
        
        // Then
        assertNotNull(response);
        assertEquals("대기중", response.getStatus());
    }
}
```

---

## 다음 단계

1. 이 가이드를 참고하여 나머지 클래스들을 구현하세요
2. 각 클래스 구현 후 단위 테스트를 작성하세요
3. 모든 구현이 완료되면 Build & Test 단계로 진행하세요

---

## 참고 문서

- Functional Design: `aidlc-docs/construction/backend/functional-design/`
- NFR Design: `aidlc-docs/construction/backend/nfr-design/`
- Infrastructure Design: `aidlc-docs/construction/backend/infrastructure-design/`
