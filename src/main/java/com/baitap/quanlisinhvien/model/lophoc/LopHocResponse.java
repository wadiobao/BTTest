package com.baitap.quanlisinhvien.model.lophoc;

import java.time.LocalDate;
import java.util.List;

import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.model.khoa.KhoaResponse;
import com.fasterxml.jackson.annotation.JsonFormat;

import jakarta.persistence.ManyToMany;
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
public class LopHocResponse {
	String maLop;
	LocalDate ngayBatDau;
	LocalDate ngayKetThuc;
	int siSo;
	List<SinhVien> dsSinhVien;
}
