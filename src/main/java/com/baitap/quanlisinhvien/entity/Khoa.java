package com.baitap.quanlisinhvien.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
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
@Table(name = "khoa")
public class Khoa {
	
	@Id
	String maKhoa;
	String tenKhoa;
	
	@OneToMany(mappedBy = "khoa",cascade = CascadeType.ALL)
	List<MonHoc> dsMonHoc;
	
	@OneToMany(mappedBy = "khoa",cascade = CascadeType.ALL)
	List<GiangVien> dsGiangVien;
	
	@OneToMany(mappedBy = "khoa",cascade = CascadeType.ALL )
	List<SinhVien> dsSinhVien;
}