package com.baitap.quanlisinhvien.model.lophoc;

import java.time.LocalDate;
import java.util.Map;

import com.baitap.quanlisinhvien.model.khoa.KhoaResponse;
import com.fasterxml.jackson.annotation.JsonFormat;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Size;
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
	String phong;
	@Min(value = 1, message = "Tiet bat dau phai tu 1")
	@Max(value = 9, message = "Tiet bau dau toi da la 9")
	int tietBatDau;
	@Min(value = 2, message = "Tiet ket thuc phai tu 2")
	@Max(value = 10, message = "Tiet ket thuc toi da la 10") 
	int tietKetThuc;
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngayBatDau;
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngayKetThuc;
	@Min(value = 25, message = "Si so phai lon hon 25")
	int siSo;
	Map<Long,String> dsSinhVien;
}
