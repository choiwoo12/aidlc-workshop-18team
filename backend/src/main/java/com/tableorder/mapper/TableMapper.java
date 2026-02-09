package com.tableorder.mapper;

import com.tableorder.domain.Table;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface TableMapper {
    
    Table findById(@Param("id") Long id);
}
