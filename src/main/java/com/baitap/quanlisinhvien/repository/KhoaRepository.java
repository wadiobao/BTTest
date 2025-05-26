package com.baitap.quanlisinhvien.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.baitap.quanlisinhvien.entity.Khoa;

public interface KhoaRepository extends JpaRepository<Khoa, String>{
	boolean existsByTenKhoa(String tenKhoa);
	Optional<Khoa> findByTenKhoa(String tenKhoa);
}
