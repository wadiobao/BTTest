package com.baitap.quanlisinhvien.repository;

import java.util.List;
import java.util.Optional;


import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.baitap.quanlisinhvien.entity.SinhVien;

@Repository
public interface SinhVienRepository extends JpaRepository<SinhVien, Long> {
	Optional<SinhVien> findByHoTen(String hoTen);
	Optional<List<SinhVien>> findAllByHoTen(String hoTen);
	Optional<List<SinhVien>> findAllByHoTenContainingIgnoreCase(String hoTen);
	Page<SinhVien> findAllByHoTenContainingIgnoreCase(String hoTen,Pageable pageable);
}
