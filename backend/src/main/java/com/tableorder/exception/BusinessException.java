package com.tableorder.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

/**
 * 비즈니스 예외 클래스
 */
@Getter
public class BusinessException extends RuntimeException {
    
    private final HttpStatus httpStatus;
    private final String errorCode;
    
    public BusinessException(String message) {
        this(message, HttpStatus.BAD_REQUEST, "BUSINESS_ERROR");
    }
    
    public BusinessException(String message, HttpStatus httpStatus) {
        this(message, httpStatus, "BUSINESS_ERROR");
    }
    
    public BusinessException(String message, HttpStatus httpStatus, String errorCode) {
        super(message);
        this.httpStatus = httpStatus;
        this.errorCode = errorCode;
    }
}
