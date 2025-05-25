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
import com.baitap.quanlisinhvien.model.lophoc.LopHocRequest;
import com.baitap.quanlisinhvien.model.monhoc.MonHocRequest;
import com.baitap.quanlisinhvien.service.LopHocService;
import com.baitap.quanlisinhvien.service.MonHocService;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@RestController
@RequestMapping("/monhoc")
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class MonHocController {
	MonHocService monHocService;
	
	@GetMapping("/tatca")
	public CustomResponse<Object> hienThiTatCaMonHoc(){
		return monHocService.hienThiTatCaMonHoc();
	}
	
	@PostMapping("/themmonhoc")
	public CustomResponse<Object> themMonHoc(@RequestBody MonHocRequest monHocRequest){
		return monHocService.themMonHoc(monHocRequest);
	}
	
	@DeleteMapping("xoa/{id}")
	public CustomResponse<Object> xoaMonHoc(@PathVariable("id") String id){
		return monHocService.xoaMonHoc(id);
	} 
	
	@PutMapping("/sua/{id}")
	public CustomResponse<Object> xoaMonHoc(@PathVariable("id") String id,@RequestBody MonHocRequest monHocRequest){
		return monHocService.suaMonHoc(id, monHocRequest);
	} 
}
