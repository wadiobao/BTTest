package com.baitap.quanlisinhvien.model.sinhvien;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

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
	String gioiTinh;
	LocalDate ngaySinh;
	String email;
	String diaChi;
	String sdt;
	String tenKhoa;
	Map<String,String> tenLopDangHoc;
	Map<String,Float> diem;
	
}
