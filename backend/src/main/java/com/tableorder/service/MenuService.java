package com.tableorder.service;

import com.tableorder.domain.Menu;
import com.tableorder.dto.menu.MenuResponse;
import com.tableorder.exception.BusinessException;
import com.tableorder.mapper.MenuMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class MenuService {

    private final MenuMapper menuMapper;

    @Cacheable(value = "menus", key = "#storeId")
    @Transactional(readOnly = true)
    public List<MenuResponse> getMenusByStore(Long storeId) {
        log.info("Getting menus for storeId: {}", storeId);
        
        List<Menu> menus = menuMapper.findByStoreId(storeId);
        return menus.stream()
                .filter(menu -> !menu.isDeleted())
                .map(this::toMenuResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public MenuResponse getMenuById(Long menuId) {
        log.info("Getting menu by id: {}", menuId);
        
        Menu menu = menuMapper.findById(menuId);
        if (menu == null) {
            throw new BusinessException("Menu not found: " + menuId);
        }
        if (menu.isDeleted()) {
            throw new BusinessException("Menu is deleted: " + menuId);
        }
        
        return toMenuResponse(menu);
    }

    private MenuResponse toMenuResponse(Menu menu) {
        return MenuResponse.builder()
                .id(menu.getId())
                .storeId(menu.getStoreId())
                .name(menu.getName())
                .price(menu.getPrice())
                .imageUrl(menu.getImageUrl())
                .createdAt(menu.getCreatedAt())
                .build();
    }
}
