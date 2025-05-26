package com.baitap.quanlisinhvien.model.giangvien;

import java.time.LocalDate;

import com.baitap.quanlisinhvien.entity.Khoa;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.FieldDefaults;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@FieldDefaults(level = AccessLevel.PRIVATE)
public class GiangVienResponse {
	String tenGiangVien;
	String gioiTinh;
	LocalDate ngaySinh;
	String email;
	String diaChi;
	String sdt;
	String tenKhoa;
}
