package com.baitap.quanlisinhvien.entity;

import java.time.LocalDate;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonFormat;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;
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
@Entity
@Builder
@Table(name = "lop_hoc")
@FieldDefaults(level = AccessLevel.PRIVATE)
public class LopHoc {
	
	@Id
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
	
	@ManyToMany()
	@JoinTable(name = "sinhvien_lophoc", joinColumns = @JoinColumn(name = "ma_lop"), inverseJoinColumns = @JoinColumn(name = "ma_sinh_vien"))
	List<SinhVien> dsSinhVien;
	
}
