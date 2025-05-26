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
import com.baitap.quanlisinhvien.model.lophoc.LopHocRequest;
import com.baitap.quanlisinhvien.service.KhoaService;
import com.baitap.quanlisinhvien.service.LopHocService;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@RestController
@RequestMapping("/lop")
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class LopHocController {
	LopHocService lopHocService;
	
	@GetMapping("/tatca")
	public CustomResponse<Object> hienThiTatCaMonHoc(){
		return lopHocService.hienThiTatCaLopHoc();
	}
	
	@PostMapping("/themlop")
	public CustomResponse<Object> themLopHoc(@RequestBody LopHocRequest lopHocRequest){
		return lopHocService.themLopHoc(lopHocRequest);
	}
	
	@DeleteMapping("/xoa/{id}")
	public CustomResponse<Object> xoaLopHoc(@PathVariable("id") String id  ){
		return lopHocService.xoaLopHoc(id);
	} 
	
	@PutMapping("sua/{id}")
	public CustomResponse<Object> suaLopHoc(@PathVariable("id") String id,@RequestBody LopHocRequest lopHocRequest){
		return lopHocService.suaLopHoc(id,lopHocRequest);
	} 
}
