package com.baitap.quanlisinhvien.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;


import com.baitap.quanlisinhvien.entity.MonHoc;

public interface MonHocRepository extends JpaRepository<MonHoc, String> {
	boolean existsByTenMonHoc(String tenMonHoc);
	Optional<MonHoc> findByTenMonHoc(String tenMonHoc);
}
