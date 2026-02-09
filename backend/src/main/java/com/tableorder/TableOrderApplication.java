package com.tableorder;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Table Order Backend Application
 */
@SpringBootApplication
@EnableCaching
@EnableRetry
@EnableAsync
public class TableOrderApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(TableOrderApplication.class, args);
    }
}
