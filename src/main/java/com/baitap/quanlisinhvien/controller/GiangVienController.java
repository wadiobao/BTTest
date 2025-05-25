package com.baitap.quanlisinhvien.controller;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.giangvien.GiangVienRequest;
import com.baitap.quanlisinhvien.model.sinhvien.SinhVienRequest;
import com.baitap.quanlisinhvien.service.GiangVienService;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@RestController
@RequestMapping("/giangvien")
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class GiangVienController {
	GiangVienService giangVienService;
	
	@GetMapping("/tatca")
	public CustomResponse<Object> hienThiTatCaGiangVien(){
		return giangVienService.hienThiTatCaGiangVien();
	}
	
	@PostMapping("/them")
	public CustomResponse<Object> themSinhVien(@RequestBody GiangVienRequest giangVienRequest){
		return giangVienService.themGiangVien(giangVienRequest);
	}
	
	@DeleteMapping("/xoa/{id}")
	public CustomResponse<Object> xoaGiangVien(@PathVariable("id") Long id){
		return giangVienService.xoaGiangVien(id);
	}
	
	@PutMapping("/sua/{id}")
	public CustomResponse<Object> suaThongTinGiangVien(@PathVariable("id") Long id, @RequestBody GiangVienRequest giangVienRequest){
		return giangVienService.suaGiangVien(id, giangVienRequest);
	}
}
