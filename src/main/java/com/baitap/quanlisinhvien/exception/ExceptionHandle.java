package com.baitap.quanlisinhvien.exception;

import com.baitap.quanlisinhvien.enums.ErrorCode;

public class ExceptionHandle extends RuntimeException {
	private ErrorCode errorCode;

	public ExceptionHandle(ErrorCode code) {
		super();
		this.errorCode = code;
	}

	public ErrorCode getErrorCode() {
		return errorCode;
	}

	public void setErrorCod(ErrorCode code) {
		this.errorCode = code;
	}
}
