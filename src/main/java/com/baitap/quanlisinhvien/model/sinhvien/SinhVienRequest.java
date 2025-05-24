package com.baitap.quanlisinhvien.model.sinhvien;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

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
	String gioiTinh;
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngaySinh;
	String email;
	String diaChi;
	String sdt;
	String tenKhoa;
	Map<String,Float> diem;
}
