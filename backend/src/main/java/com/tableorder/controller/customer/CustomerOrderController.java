package com.tableorder.controller.customer;

import com.tableorder.dto.ApiResponse;
import com.tableorder.dto.order.CreateOrderRequest;
import com.tableorder.dto.order.OrderResponse;
import com.tableorder.service.OrderService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/customer/orders")
@RequiredArgsConstructor
@Tag(name = "Customer Order", description = "고객 주문 API")
public class CustomerOrderController {

    private final OrderService orderService;

    @PostMapping
    @Operation(summary = "주문 생성", description = "고객이 메뉴를 선택하여 주문을 생성합니다")
    public ResponseEntity<ApiResponse<OrderResponse>> createOrder(
            @Validated @RequestBody CreateOrderRequest request) {
        log.info("POST /api/customer/orders - sessionId: {}", request.getSessionId());
        
        OrderResponse response = orderService.createOrder(request);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "세션별 주문 조회", description = "특정 세션의 모든 주문을 조회합니다")
    public ResponseEntity<ApiResponse<List<OrderResponse>>> getOrdersBySession(
            @RequestParam String sessionId) {
        log.info("GET /api/customer/orders?sessionId={}", sessionId);
        
        List<OrderResponse> orders = orderService.getOrdersBySession(sessionId);
        return ResponseEntity.ok(ApiResponse.success(orders));
    }

    @GetMapping("/{orderId}")
    @Operation(summary = "주문 상세 조회", description = "주문 ID로 주문 상세 정보를 조회합니다")
    public ResponseEntity<ApiResponse<OrderResponse>> getOrderById(
            @PathVariable Long orderId) {
        log.info("GET /api/customer/orders/{}", orderId);
        
        OrderResponse order = orderService.getOrderById(orderId);
        return ResponseEntity.ok(ApiResponse.success(order));
    }
}
