package com.baitap.quanlisinhvien.entity;

import java.time.LocalDate;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonFormat;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;
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
	
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngayBatDau;
	

	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngayKetThuc;
	
	int siSo;
	
	@ManyToMany(mappedBy = "dsLopHoc")
	List<SinhVien> dsSinhVien;
	
}
