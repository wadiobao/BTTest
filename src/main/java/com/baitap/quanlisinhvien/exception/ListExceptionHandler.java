package com.baitap.quanlisinhvien.exception;

import java.util.NoSuchElementException;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import com.baitap.quanlisinhvien.enums.ErrorCode;
import com.baitap.quanlisinhvien.model.CustomResponse;


@ControllerAdvice
public class ListExceptionHandler {

	@SuppressWarnings("rawtypes")
	@ExceptionHandler(exception = NoSuchElementException.class)
	ResponseEntity<CustomResponse> handlingNoSuchElementException(NoSuchElementException exception) {
		CustomResponse response = new CustomResponse();
		response.setLoiNhan(exception.getMessage());
		return ResponseEntity.badRequest().body(response);
	}
	
	@SuppressWarnings("rawtypes")
	@ExceptionHandler(exception = ExceptionHandle.class)
	ResponseEntity<CustomResponse> handlingExceptionHandle(ExceptionHandle exception) {
		CustomResponse response = new CustomResponse();
		ErrorCode code = exception.getErrorCode();
		response.setCode(code.getCode());
		response.setLoiNhan(code.getMessage());
		return ResponseEntity.badRequest().body(response);
	}
	
	@ExceptionHandler(exception = RuntimeException.class)
	ResponseEntity<CustomResponse> handlingRuntimeException(RuntimeException exception) {
		CustomResponse response = new CustomResponse();
		response.setCode(400);
		response.setLoiNhan(exception.getMessage());
		return ResponseEntity.badRequest().body(response);
	}
}
