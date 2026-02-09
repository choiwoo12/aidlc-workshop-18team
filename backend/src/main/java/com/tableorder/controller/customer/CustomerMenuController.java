package com.tableorder.controller.customer;

import com.tableorder.dto.ApiResponse;
import com.tableorder.dto.menu.MenuResponse;
import com.tableorder.service.MenuService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/customer/menus")
@RequiredArgsConstructor
@Tag(name = "Customer Menu", description = "고객 메뉴 조회 API")
public class CustomerMenuController {

    private final MenuService menuService;

    @GetMapping
    @Operation(summary = "매장별 메뉴 조회", description = "특정 매장의 모든 메뉴를 조회합니다")
    public ResponseEntity<ApiResponse<List<MenuResponse>>> getMenusByStore(
            @RequestParam Long storeId) {
        log.info("GET /api/customer/menus?storeId={}", storeId);
        
        List<MenuResponse> menus = menuService.getMenusByStore(storeId);
        return ResponseEntity.ok(ApiResponse.success(menus));
    }

    @GetMapping("/{menuId}")
    @Operation(summary = "메뉴 상세 조회", description = "메뉴 ID로 메뉴 상세 정보를 조회합니다")
    public ResponseEntity<ApiResponse<MenuResponse>> getMenuById(
            @PathVariable Long menuId) {
        log.info("GET /api/customer/menus/{}", menuId);
        
        MenuResponse menu = menuService.getMenuById(menuId);
        return ResponseEntity.ok(ApiResponse.success(menu));
    }
}
