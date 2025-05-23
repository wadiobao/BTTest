package com.baitap.quanlisinhvien.entity;

import java.time.LocalDate;

import com.fasterxml.jackson.annotation.JsonFormat;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
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
@Table(name = "sinh_vien")
@FieldDefaults(level = AccessLevel.PRIVATE)
public class SinhVien {
	
	@Id
	@GeneratedValue(strategy = GenerationType.UUID)
	String id;
	
	String hoTen;
	
	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngaySinh;
	
	String email;
	
	String diaChi;
	
	String sdt;
	
	
}
