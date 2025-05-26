package com.baitap.quanlisinhvien.model;

import java.time.LocalDate;

import com.fasterxml.jackson.annotation.JsonFormat;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.FieldDefaults;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
@FieldDefaults(level = AccessLevel.PRIVATE)
public class SinhVienRequest {
	String hoTen;
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngaySinh;
	String email;
	String diaChi;
	String sdt;
}
