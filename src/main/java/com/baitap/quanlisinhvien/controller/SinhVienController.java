package com.baitap.quanlisinhvien.controller;


import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.sinhvien.SinhVienRequest;
import com.baitap.quanlisinhvien.service.SinhVienService;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@RestController
@RequestMapping("/sinhvien")
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class SinhVienController {
	
	SinhVienService sinhVienService;
	
	@PostMapping("/themsinhvien")
	public CustomResponse<Object> themSinhVien(@RequestBody SinhVienRequest sinhVienRequest){
		return sinhVienService.themSinhVien(sinhVienRequest);
	}
	
	@PutMapping("/suathongtin/{id}")
	public CustomResponse<Object> suaThongTinSinhVien(@PathVariable("id") Long id, @RequestBody SinhVienRequest sinhVienRequest){
		return sinhVienService.suaThongTinSinhVien(id,sinhVienRequest);
	}
	
	@DeleteMapping("/xoasinhvien/{id}")
	public CustomResponse<Object> xoaSinhVien(@PathVariable("id") Long id){
		return sinhVienService.xoaSinhVien(id);
	}
	
	@GetMapping("/tatcasinhvien")
	public CustomResponse<Object> hienThiTatCaSinhVien(){
		return sinhVienService.hienThiTatCaSinhVien();
	}
	
	@PostMapping("/thongtin/{id}")
	public CustomResponse<Object> hienThiThongTinSinhVienTheoId(@PathVariable("id") Long id){
		return sinhVienService.hienThiThongTinSinhVienTheoId(id);
	}
	
	@PostMapping("/thongtin/hoten")
	public CustomResponse<Object> hienThiThongTinCacSinhVienTheoTen(@RequestParam String hoTen){
		return sinhVienService.hienThiThongTinCacSinhVienTheoTen(hoTen);
	}
	
	@GetMapping("/thongtin/hoten/phantrang")
	public CustomResponse<Object> hienThiThongTinCacSinhVienTheoTenPhanTrang(
	    @RequestParam String hoTen,
	    @RequestParam(defaultValue = "0") int page,
	    @RequestParam(defaultValue = "10") int size,
	    @RequestParam(defaultValue = "hoTen") String sortBy,
	    @RequestParam(defaultValue = "asc") String direction
	) {
	    return sinhVienService.hienThiThongTinCacSinhVienTheoTenPhanTrang(hoTen, page, size, sortBy, direction);
	}
}
