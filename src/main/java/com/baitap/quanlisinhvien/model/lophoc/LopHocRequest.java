package com.baitap.quanlisinhvien.model.lophoc;

import java.time.LocalDate;

import com.baitap.quanlisinhvien.model.khoa.KhoaResponse;
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
public class LopHocRequest {
	String maLop;
	String tenLop;
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngayBatDau;
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngayKetThuc;
	int siSo;
}
