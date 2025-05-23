package com.baitap.quanlisinhvien.enums;

public enum ErrorCode {
	KHONG_TIM_THAY(400,"Khong tim thay sinh vien")
	;
	private int code;
	private String message;
	
	private ErrorCode(int code, String message) {
		this.code = code;
		this.message = message;
	}

	public int getCode() {
		return code;
	}

	public void setCode(int code) {
		this.code = code;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}
	
	
	
	
}
