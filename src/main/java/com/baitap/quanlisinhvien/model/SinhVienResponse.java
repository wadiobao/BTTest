package com.baitap.quanlisinhvien.model;

import java.time.LocalDate;

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
public class SinhVienResponse {
	String hoTen;
	LocalDate ngaySinh;
	String email;
	String diaChi;
	String sdt;
}
