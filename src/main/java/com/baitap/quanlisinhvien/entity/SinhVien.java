package com.baitap.quanlisinhvien.entity;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonFormat;

import jakarta.persistence.CollectionTable;
import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.MapKeyColumn;
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
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	Long maSinhVien;

	String hoTen;

	String gioiTinh;

	@JsonFormat(pattern = "dd/MM/yyyy")
	LocalDate ngaySinh;

	String email;

	String diaChi;

	String sdt;

	@ManyToMany(mappedBy = "dsSinhVien")	
	List<LopHoc> dsLopHoc;
	
	
	@ElementCollection
    @CollectionTable(name = "diem_mon_hoc", joinColumns = @JoinColumn(name = "ma_sinh_vien"))
    @MapKeyColumn(name = "mon_hoc")
    @Column(name = "diem")
    Map<String, Float> diemMonHoc;
	
	@ManyToOne
	@JoinColumn(name = "ma_khoa")
	Khoa khoa;

}
