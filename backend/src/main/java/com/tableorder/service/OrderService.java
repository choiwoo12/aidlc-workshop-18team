package com.tableorder.service;

import com.tableorder.domain.Order;
import com.tableorder.domain.OrderItem;
import com.tableorder.dto.order.CreateOrderRequest;
import com.tableorder.dto.order.OrderItemRequest;
import com.tableorder.dto.order.OrderResponse;
import com.tableorder.dto.order.OrderItemResponse;
import com.tableorder.exception.BusinessException;
import com.tableorder.mapper.OrderMapper;
import com.tableorder.mapper.MenuMapper;
import com.tableorder.mapper.TableMapper;
import com.tableorder.util.OrderNumberGenerator;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderMapper orderMapper;
    private final MenuMapper menuMapper;
    private final TableMapper tableMapper;
    private final OrderNumberGenerator orderNumberGenerator;

    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        log.info("Creating order for sessionId: {}, tableId: {}", request.getSessionId(), request.getTableId());

        // 1. Validate session
        validateSession(request.getSessionId(), request.getTableId());

        // 2. Validate menu items
        validateMenuItems(request.getItems());

        // 3. Create order
        Order order = new Order();
        order.setOrderNumber(orderNumberGenerator.generate());
        order.setTableId(request.getTableId());
        order.setSessionId(request.getSessionId());
        order.setStatus("PENDING");
        order.setCreatedAt(LocalDateTime.now());

        // 4. Calculate total amount and create order items
        int totalAmount = 0;
        for (OrderItemRequest itemRequest : request.getItems()) {
            var menu = menuMapper.findById(itemRequest.getMenuId());
            if (menu == null) {
                throw new BusinessException("Menu not found: " + itemRequest.getMenuId());
            }
            totalAmount += menu.getPrice() * itemRequest.getQuantity();
        }
        order.setTotalAmount(totalAmount);

        // 5. Insert order
        orderMapper.insert(order);

        // 6. Insert order items
        for (OrderItemRequest itemRequest : request.getItems()) {
            var menu = menuMapper.findById(itemRequest.getMenuId());
            OrderItem orderItem = new OrderItem();
            orderItem.setOrderId(order.getId());
            orderItem.setMenuId(itemRequest.getMenuId());
            orderItem.setQuantity(itemRequest.getQuantity());
            orderItem.setUnitPrice(menu.getPrice());
            orderItem.setCreatedAt(LocalDateTime.now());
            orderMapper.insertOrderItem(orderItem);
        }

        log.info("Order created successfully: {}", order.getOrderNumber());

        return toOrderResponse(order);
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getOrdersBySession(String sessionId) {
        log.info("Getting orders for sessionId: {}", sessionId);
        
        List<Order> orders = orderMapper.findBySessionId(sessionId);
        return orders.stream()
                .map(this::toOrderResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrderById(Long orderId) {
        log.info("Getting order by id: {}", orderId);
        
        Order order = orderMapper.findById(orderId);
        if (order == null) {
            throw new BusinessException("Order not found: " + orderId);
        }
        
        return toOrderResponse(order);
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getRecentOrders(Long storeId, int limit) {
        log.info("Getting recent {} orders for storeId: {}", limit, storeId);
        
        List<Order> orders = orderMapper.findRecentByStoreId(storeId, limit);
        return orders.stream()
                .map(this::toOrderResponse)
                .collect(Collectors.toList());
    }

    private void validateSession(String sessionId, Long tableId) {
        var table = tableMapper.findById(tableId);
        if (table == null) {
            throw new BusinessException("Table not found: " + tableId);
        }
        if (!table.isSessionActive()) {
            throw new BusinessException("Table session is not active");
        }
        if (!sessionId.equals(table.getSessionId())) {
            throw new BusinessException("Invalid session ID");
        }
    }

    private void validateMenuItems(List<OrderItemRequest> items) {
        if (items == null || items.isEmpty()) {
            throw new BusinessException("Order items cannot be empty");
        }
        
        for (OrderItemRequest item : items) {
            if (item.getQuantity() <= 0) {
                throw new BusinessException("Invalid quantity: " + item.getQuantity());
            }
            
            var menu = menuMapper.findById(item.getMenuId());
            if (menu == null) {
                throw new BusinessException("Menu not found: " + item.getMenuId());
            }
            if (menu.isDeleted()) {
                throw new BusinessException("Menu is deleted: " + item.getMenuId());
            }
        }
    }

    private OrderResponse toOrderResponse(Order order) {
        List<OrderItem> items = orderMapper.findOrderItemsByOrderId(order.getId());
        
        List<OrderItemResponse> itemResponses = items.stream()
                .map(item -> {
                    var menu = menuMapper.findById(item.getMenuId());
                    return OrderItemResponse.builder()
                            .id(item.getId())
                            .menuId(item.getMenuId())
                            .menuName(menu != null ? menu.getName() : "Unknown")
                            .quantity(item.getQuantity())
                            .unitPrice(item.getUnitPrice())
                            .subtotal(item.getUnitPrice() * item.getQuantity())
                            .build();
                })
                .collect(Collectors.toList());

        return OrderResponse.builder()
                .id(order.getId())
                .orderNumber(order.getOrderNumber())
                .tableId(order.getTableId())
                .sessionId(order.getSessionId())
                .status(order.getStatus())
                .totalAmount(order.getTotalAmount())
                .items(itemResponses)
                .createdAt(order.getCreatedAt())
                .build();
    }
}
