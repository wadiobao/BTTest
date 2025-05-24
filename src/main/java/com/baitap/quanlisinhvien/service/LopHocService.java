package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.entity.LopHoc;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.khoa.KhoaRequest;
import com.baitap.quanlisinhvien.model.lophoc.LopHocRequest;
import com.baitap.quanlisinhvien.repository.LopHocRepository;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class LopHocService {
	LopHocRepository lopHocRepository;

	public CustomResponse<Object> hienThiTatCaLopHoc() {
		List<LopHoc> danhSachLopHoc = lopHocRepository.findAll();
		return CustomResponse.builder().ketQua(danhSachLopHoc).loiNhan("Hien thi tat ca lop hoc").build();
	}

	public CustomResponse<Object> themKhoa(LopHocRequest lopHocRequest) {

		LopHoc lopHocMoi = LopHoc.builder()
				.maLop(lopHocRequest.getMaLop())
				.tenLop(lopHocRequest.getTenLop())
				.ngayBatDau(lopHocRequest.getNgayBatDau())
				.ngayKetThuc(lopHocRequest.getNgayKetThuc())
				.siSo(lopHocRequest.getSiSo())
				.dsSinhVien(new ArrayList<>())
				.build();

		lopHocRepository.save(lopHocMoi);

		return CustomResponse.builder().ketQua(lopHocMoi).loiNhan("Them lop hoc moi thanh cong").build();
	}
}
