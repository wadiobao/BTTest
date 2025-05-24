package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.entity.MonHoc;
import com.baitap.quanlisinhvien.enums.ErrorCode;
import com.baitap.quanlisinhvien.exception.ExceptionHandle;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.monhoc.MonHocRequest;
import com.baitap.quanlisinhvien.model.monhoc.MonHocResponse;
import com.baitap.quanlisinhvien.repository.KhoaRepository;
import com.baitap.quanlisinhvien.repository.MonHocRepository;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class MonHocService {
	MonHocRepository monHocRepository;
	KhoaRepository khoaRepository;
	
	public CustomResponse<Object> hienThiTatCaMonHoc() {
		List<MonHoc> danhSachMonHoc = monHocRepository.findAll();
		List<MonHocResponse> danhSachMonHocResponses = new ArrayList<MonHocResponse>();
		for (MonHoc monHoc : danhSachMonHoc) {
			MonHocResponse monHocResponse = MonHocResponse.builder()
					.maMonHoc(monHoc.getMaMonHoc())
					.tenMonHoc(monHoc.getTenMonHoc())
					.tenKhoa(monHoc.getKhoa().getTenKhoa())
					.build();
			danhSachMonHocResponses.add(monHocResponse);
		}
		return CustomResponse.builder().ketQua(danhSachMonHocResponses).loiNhan("Hien thi tat ca mon hoc").build();
	}
	
	public CustomResponse<Object> themMonHoc(MonHocRequest monHocRequest) {
		if (monHocRepository.existsByTenMonHoc(monHocRequest.getTenMonHoc()))
			throw new RuntimeException("Da ton tai ten mon hoc");
		else if(monHocRepository.existsById(monHocRequest.getMaMonHoc()))
			throw new RuntimeException("Da ton tai ma mon hoc");

		Khoa khoa = khoaRepository.findByTenKhoa(monHocRequest.getTenKhoa())
				.orElseThrow(() -> new ExceptionHandle(ErrorCode.KHOA_KHONG_TON_TAI));
		
		MonHoc monHocMoi = MonHoc.builder()
				.maMonHoc(monHocRequest.getMaMonHoc())
				.tenMonHoc(monHocRequest.getTenMonHoc())
				.khoa(khoa)
				.build();

		monHocRepository.save(monHocMoi);
		
		MonHocResponse monHocResponse = MonHocResponse.builder()
				.maMonHoc(monHocMoi.getMaMonHoc())
				.tenMonHoc(monHocMoi.getTenMonHoc())
				.tenKhoa(monHocMoi.getKhoa().getTenKhoa())
				.build();

		return CustomResponse.builder().ketQua(monHocResponse).loiNhan("Them mon hoc moi thanh cong").build();
	}
}
