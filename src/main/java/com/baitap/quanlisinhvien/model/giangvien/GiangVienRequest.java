package com.baitap.quanlisinhvien.model.giangvien;

import java.time.LocalDate;

import com.fasterxml.jackson.annotation.JsonFormat;

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
public class GiangVienRequest {
	String tenGiangVien;
	String gioiTinh;
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngaySinh;
	String email;
	String diaChi;
	String sdt;
	String tenKhoa;
}
