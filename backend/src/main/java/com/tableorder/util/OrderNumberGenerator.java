package com.tableorder.util;

import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.atomic.AtomicInteger;

@Component
public class OrderNumberGenerator {
    
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyyMMdd");
    private final AtomicInteger sequence = new AtomicInteger(0);
    private String lastDate = "";

    public synchronized String generate() {
        LocalDateTime now = LocalDateTime.now();
        String currentDate = now.format(DATE_FORMATTER);
        
        // Reset sequence if date changed
        if (!currentDate.equals(lastDate)) {
            sequence.set(0);
            lastDate = currentDate;
        }
        
        int seq = sequence.incrementAndGet();
        return String.format("ORD-%s-%04d", currentDate, seq);
    }
}
