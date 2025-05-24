package com.baitap.quanlisinhvien.entity;

import java.time.LocalDate;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonFormat;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Builder
@Table(name = "giang_vien")
public class GiangVien {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	Long maGiangVien;
	String tenGiangVien;
	String gioiTinh;

	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngaySinh;

	String email;

	String diaChi;

	String sdt;
	
	@ManyToOne
	@JoinColumn(name = "ma_khoa")
	Khoa khoa;
}
