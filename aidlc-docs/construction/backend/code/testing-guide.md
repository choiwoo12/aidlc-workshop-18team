# Backend Testing Guide

## Overview
Backend 유닛의 테스트 작성 가이드입니다. 단위 테스트와 통합 테스트 작성 방법을 설명합니다.

---

## Test Structure

```
backend/src/test/java/com/tableorder/
├── controller/
│   ├── CustomerOrderControllerTest.java
│   ├── AdminOrderControllerTest.java
│   └── AdminMenuControllerTest.java
├── service/
│   ├── OrderServiceTest.java
│   ├── MenuServiceTest.java
│   └── TableServiceTest.java
└── util/
    ├── OrderNumberGeneratorTest.java
    └── HashUtilTest.java
```

---

## 1. Service Layer Tests

### 1.1 OrderServiceTest 예시

```java
package com.tableorder.service;

import com.tableorder.domain.Order;
import com.tableorder.domain.Menu;
import com.tableorder.domain.Table;
import com.tableorder.dto.order.CreateOrderRequest;
import com.tableorder.dto.order.OrderItemRequest;
import com.tableorder.dto.order.OrderResponse;
import com.tableorder.exception.InvalidSessionException;
import com.tableorder.exception.MenuNotFoundException;
import com.tableorder.infrastructure.sse.SSEService;
import com.tableorder.mapper.MenuMapper;
import com.tableorder.mapper.OrderMapper;
import com.tableorder.mapper.TableMapper;
import com.tableorder.util.OrderNumberGenerator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    
    @Mock
    private OrderMapper orderMapper;
    
    @Mock
    private MenuMapper menuMapper;
    
    @Mock
    private TableMapper tableMapper;
    
    @Mock
    private SSEService sseService;
    
    @Mock
    private OrderNumberGenerator orderNumberGenerator;
    
    @InjectMocks
    private OrderService orderService;
    
    private CreateOrderRequest request;
    private Table table;
    private Menu menu;
    
    @BeforeEach
    void setUp() {
        // Given: 테스트 데이터 준비
        request = new CreateOrderRequest();
        request.setStoreId(1L);
        request.setTableId(1L);
        request.setSessionId("test-session-id");
        
        OrderItemRequest item = new OrderItemRequest();
        item.setMenuId(1L);
        item.setQuantity(2);
        request.setItems(Arrays.asList(item));
        
        table = Table.builder()
                .id(1L)
                .storeId(1L)
                .sessionId("test-session-id")
                .sessionStatus("ACTIVE")
                .build();
        
        menu = Menu.builder()
                .id(1L)
                .storeId(1L)
                .name("김치찌개")
                .price(8000)
                .deleted(false)
                .build();
    }
    
    @Test
    void createOrder_Success() {
        // Given
        when(tableMapper.selectById(1L)).thenReturn(table);
        when(menuMapper.selectById(1L)).thenReturn(menu);
        when(orderNumberGenerator.generateOrderNumber(any(LocalDate.class), anyInt()))
                .thenReturn("ORD-20260209-0001");
        
        // When
        OrderResponse response = orderService.createOrder(request);
        
        // Then
        assertNotNull(response);
        assertEquals("ORD-20260209-0001", response.getOrderNumber());
        assertEquals(16000, response.getTotalAmount()); // 8000 * 2
        assertEquals("대기중", response.getStatus());
        
        verify(orderMapper, times(1)).insertOrder(any(Order.class));
        verify(sseService, times(1)).broadcastEventToStore(anyLong(), any());
    }
    
    @Test
    void createOrder_InvalidSession_ThrowsException() {
        // Given
        table.setSessionId("different-session-id");
        when(tableMapper.selectById(1L)).thenReturn(table);
        
        // When & Then
        assertThrows(InvalidSessionException.class, () -> {
            orderService.createOrder(request);
        });
        
        verify(orderMapper, never()).insertOrder(any());
    }
    
    @Test
    void createOrder_MenuNotFound_ThrowsException() {
        // Given
        when(tableMapper.selectById(1L)).thenReturn(table);
        when(menuMapper.selectById(1L)).thenReturn(null);
        
        // When & Then
        assertThrows(MenuNotFoundException.class, () -> {
            orderService.createOrder(request);
        });
        
        verify(orderMapper, never()).insertOrder(any());
    }
    
    @Test
    void createOrder_DeletedMenu_ThrowsException() {
        // Given
        menu.setDeleted(true);
        when(tableMapper.selectById(1L)).thenReturn(table);
        when(menuMapper.selectById(1L)).thenReturn(menu);
        
        // When & Then
        assertThrows(MenuNotFoundException.class, () -> {
            orderService.createOrder(request);
        });
    }
}
```

---

## 2. Controller Layer Tests

### 2.1 CustomerOrderControllerTest 예시

```java
package com.tableorder.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.tableorder.dto.order.CreateOrderRequest;
import com.tableorder.dto.order.OrderItemRequest;
import com.tableorder.dto.order.OrderResponse;
import com.tableorder.service.OrderService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(CustomerOrderController.class)
class CustomerOrderControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @MockBean
    private OrderService orderService;
    
    @Test
    void createOrder_Success() throws Exception {
        // Given
        CreateOrderRequest request = new CreateOrderRequest();
        request.setStoreId(1L);
        request.setTableId(1L);
        request.setSessionId("test-session-id");
        
        OrderItemRequest item = new OrderItemRequest();
        item.setMenuId(1L);
        item.setQuantity(2);
        request.setItems(Arrays.asList(item));
        
        OrderResponse response = OrderResponse.builder()
                .id(1L)
                .orderNumber("ORD-20260209-0001")
                .totalAmount(16000)
                .status("대기중")
                .build();
        
        when(orderService.createOrder(any())).thenReturn(response);
        
        // When & Then
        mockMvc.perform(post("/api/customer/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data.orderNumber").value("ORD-20260209-0001"))
                .andExpect(jsonPath("$.data.totalAmount").value(16000))
                .andExpect(jsonPath("$.data.status").value("대기중"));
    }
    
    @Test
    void createOrder_ValidationFailed() throws Exception {
        // Given: 빈 요청 (필수 필드 누락)
        CreateOrderRequest request = new CreateOrderRequest();
        
        // When & Then
        mockMvc.perform(post("/api/customer/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.success").value(false))
                .andExpect(jsonPath("$.message").value("입력 검증 실패"));
    }
}
```

---

## 3. Utility Tests

### 3.1 OrderNumberGeneratorTest 예시

```java
package com.tableorder.util;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

class OrderNumberGeneratorTest {
    
    private final OrderNumberGenerator generator = new OrderNumberGenerator();
    
    @Test
    void generateOrderNumber_Success() {
        // Given
        LocalDate date = LocalDate.of(2026, 2, 9);
        int sequence = 1;
        
        // When
        String orderNumber = generator.generateOrderNumber(date, sequence);
        
        // Then
        assertEquals("ORD-20260209-0001", orderNumber);
    }
    
    @Test
    void generateOrderNumber_LargeSequence() {
        // Given
        LocalDate date = LocalDate.of(2026, 2, 9);
        int sequence = 9999;
        
        // When
        String orderNumber = generator.generateOrderNumber(date, sequence);
        
        // Then
        assertEquals("ORD-20260209-9999", orderNumber);
    }
}
```

### 3.2 HashUtilTest 예시

```java
package com.tableorder.util;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class HashUtilTest {
    
    @Test
    void sha256_Success() {
        // Given
        String input = "1234";
        
        // When
        String hash = HashUtil.sha256(input);
        
        // Then
        assertNotNull(hash);
        assertEquals(64, hash.length()); // SHA-256 produces 64 hex characters
        assertEquals("03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", hash);
    }
    
    @Test
    void sha256_SameInputProducesSameHash() {
        // Given
        String input = "test";
        
        // When
        String hash1 = HashUtil.sha256(input);
        String hash2 = HashUtil.sha256(input);
        
        // Then
        assertEquals(hash1, hash2);
    }
}
```

---

## 4. Integration Tests

### 4.1 OrderIntegrationTest 예시

```java
package com.tableorder.integration;

import com.tableorder.dto.order.CreateOrderRequest;
import com.tableorder.dto.order.OrderItemRequest;
import com.tableorder.dto.order.OrderResponse;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class OrderIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    void createOrder_EndToEnd_Success() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest();
        request.setStoreId(1L);
        request.setTableId(1L);
        request.setSessionId("test-session-id");
        
        OrderItemRequest item = new OrderItemRequest();
        item.setMenuId(1L);
        item.setQuantity(2);
        request.setItems(Arrays.asList(item));
        
        // When
        ResponseEntity<OrderResponse> response = restTemplate.postForEntity(
                "/api/customer/orders",
                request,
                OrderResponse.class
        );
        
        // Then
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("대기중", response.getBody().getStatus());
    }
}
```

---

## 5. Test Configuration

### 5.1 application-test.yml

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:
  
  h2:
    console:
      enabled: false
  
  sql:
    init:
      mode: always

jwt:
  secret: test-secret-key
  expiration: 3600000

logging:
  level:
    com.tableorder: DEBUG
```

---

## 6. Running Tests

### 6.1 Run All Tests
```bash
mvn test
```

### 6.2 Run Specific Test Class
```bash
mvn test -Dtest=OrderServiceTest
```

### 6.3 Run Specific Test Method
```bash
mvn test -Dtest=OrderServiceTest#createOrder_Success
```

### 6.4 Run with Coverage
```bash
mvn test jacoco:report
```

---

## 7. Test Coverage Goals

- **Service Layer**: 80% coverage
- **Controller Layer**: 70% coverage
- **Utility Layer**: 90% coverage
- **Overall**: 75% coverage

---

## 8. Best Practices

### 8.1 Test Naming Convention
```
methodName_Scenario_ExpectedResult
```

예시:
- `createOrder_Success`
- `createOrder_InvalidSession_ThrowsException`
- `updateOrderStatus_OptimisticLock_ThrowsException`

### 8.2 AAA Pattern
모든 테스트는 Arrange-Act-Assert 패턴을 따릅니다:
```java
@Test
void testMethod() {
    // Arrange (Given): 테스트 데이터 준비
    
    // Act (When): 테스트 대상 메서드 실행
    
    // Assert (Then): 결과 검증
}
```

### 8.3 Mock vs Real Objects
- **Unit Tests**: Mock 사용 (Mockito)
- **Integration Tests**: Real objects 사용 (Spring Context)

### 8.4 Test Data
- 테스트 데이터는 각 테스트 메서드에서 독립적으로 생성
- `@BeforeEach`에서 공통 데이터 준비
- 테스트 간 의존성 없음

---

## 9. Common Test Utilities

### 9.1 TestDataBuilder

```java
public class TestDataBuilder {
    
    public static Order createTestOrder() {
        return Order.builder()
                .id(1L)
                .orderNumber("ORD-20260209-0001")
                .storeId(1L)
                .tableId(1L)
                .sessionId("test-session-id")
                .totalAmount(16000)
                .status("대기중")
                .version(0)
                .deleted(false)
                .build();
    }
    
    public static Menu createTestMenu() {
        return Menu.builder()
                .id(1L)
                .storeId(1L)
                .name("김치찌개")
                .price(8000)
                .deleted(false)
                .build();
    }
}
```

---

## 10. Next Steps

1. **Service Tests 작성**: 모든 Service 클래스에 대한 단위 테스트
2. **Controller Tests 작성**: 모든 Controller에 대한 단위 테스트
3. **Integration Tests 작성**: 주요 워크플로우에 대한 통합 테스트
4. **Coverage 확인**: 목표 커버리지 달성 확인
5. **Build & Test**: 전체 빌드 및 테스트 실행

---

## References

- JUnit 5: https://junit.org/junit5/
- Mockito: https://site.mockito.org/
- Spring Boot Testing: https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing
