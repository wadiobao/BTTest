package com.baitap.quanlisinhvien.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.baitap.quanlisinhvien.entity.SinhVien;

@Repository
public interface SinhVienRepository extends JpaRepository<SinhVien, String> {
	Optional<SinhVien> findByHoTen(@Param("hoTen") String hoTen);
	Optional<List<SinhVien>> findAllByHoTen(String hoTen);
	Optional<List<SinhVien>> findAllByHoTenContainingIgnoreCase(String hoTen);
}
