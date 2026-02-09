package com.tableorder.mapper;

import com.tableorder.domain.Menu;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface MenuMapper {
    
    Menu findById(@Param("id") Long id);
    
    List<Menu> findByStoreId(@Param("storeId") Long storeId);
}
