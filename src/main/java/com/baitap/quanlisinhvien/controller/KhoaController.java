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
import com.baitap.quanlisinhvien.model.khoa.KhoaRequest;
import com.baitap.quanlisinhvien.service.KhoaService;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@RestController
@RequestMapping("/khoa")
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class KhoaController {
	KhoaService khoaService;
	
	@PostMapping("/themkhoa")
	public CustomResponse<Object> themKhoa(@RequestBody KhoaRequest khoaRequest){
		return khoaService.themKhoa(khoaRequest);
	}
	
	@GetMapping("/tatca")
	public CustomResponse<Object> hienThiTatCaKhoa(){
		return khoaService.hienThiTatCaKhoa();
	}
	
	@PutMapping("/sua/{id}")
	public CustomResponse<Object> suaThongTinKhoa(@PathVariable("id") String id,@RequestBody KhoaRequest khoaRequest){
		return khoaService.suaKhoa(id,khoaRequest);
	}
	
	@DeleteMapping("/xoa/{id}")
	public CustomResponse<Object> xoaKhoa(@PathVariable("id") String id){
		return khoaService.xoaKhoa(id);
	}
}
