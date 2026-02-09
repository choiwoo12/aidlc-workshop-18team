package com.tableorder.mapper;

import com.tableorder.domain.Order;
import com.tableorder.domain.OrderItem;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface OrderMapper {
    
    void insert(Order order);
    
    void insertOrderItem(OrderItem orderItem);
    
    Order findById(@Param("id") Long id);
    
    List<Order> findBySessionId(@Param("sessionId") String sessionId);
    
    List<Order> findRecentByStoreId(@Param("storeId") Long storeId, @Param("limit") int limit);
    
    List<OrderItem> findOrderItemsByOrderId(@Param("orderId") Long orderId);
}
