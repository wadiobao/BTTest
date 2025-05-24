package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.GiangVien;
import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.enums.ErrorCode;
import com.baitap.quanlisinhvien.exception.ExceptionHandle;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.giangvien.GiangVienRequest;
import com.baitap.quanlisinhvien.model.giangvien.GiangVienResponse;
import com.baitap.quanlisinhvien.repository.GiangVienRepository;
import com.baitap.quanlisinhvien.repository.KhoaRepository;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class GiangVienService {
	GiangVienRepository giangVienRepository;

	KhoaRepository khoaRepository;

	public CustomResponse<Object> hienThiTatCaGiangVien() {
		List<GiangVien> danhSanhGiangVien = giangVienRepository.findAll();

		List<GiangVienResponse> danhSanhGiangVienResponses = new ArrayList<GiangVienResponse>();

		for (GiangVien giangVien : danhSanhGiangVien) {
			GiangVienResponse giangVienResponse = GiangVienResponse.builder()
					.tenGiangVien(giangVien.getTenGiangVien())
					.gioiTinh(giangVien.getGioiTinh())
					.ngaySinh(giangVien.getNgaySinh())
					.email(giangVien.getEmail())
					.diaChi(giangVien.getDiaChi())
					.sdt(giangVien.getSdt())
					.tenKhoa(giangVien.getKhoa().getTenKhoa())
					.build();

			danhSanhGiangVienResponses.add(giangVienResponse);
		}
		return CustomResponse.builder().ketQua(danhSanhGiangVienResponses).loiNhan("Hien thi tat ca giang vien")
				.build();
	}

	public CustomResponse<Object> themGiangVien(GiangVienRequest giangVienRequest) {

		Khoa khoa = khoaRepository.findByTenKhoa(giangVienRequest.getTenKhoa())
				.orElseThrow(() -> new ExceptionHandle(ErrorCode.KHOA_KHONG_TON_TAI));

		GiangVien giangVien = GiangVien.builder()
				.tenGiangVien(giangVienRequest.getTenGiangVien())
				.gioiTinh(giangVienRequest.getGioiTinh())
				.ngaySinh(giangVienRequest.getNgaySinh())
				.email(giangVienRequest.getEmail())
				.diaChi(giangVienRequest.getDiaChi())
				.sdt(giangVienRequest.getSdt())
				.khoa(khoa).build();

		giangVienRepository.save(giangVien);

		GiangVienResponse giangVienResponse = GiangVienResponse.builder()
				.tenGiangVien(giangVien.getTenGiangVien())
				.gioiTinh(giangVien.getGioiTinh())
				.ngaySinh(giangVien.getNgaySinh())
				.email(giangVien.getEmail())
				.diaChi(giangVien.getDiaChi())
				.sdt(giangVien.getSdt())
				.tenKhoa(giangVien.getKhoa().getTenKhoa())
				.build();

		return CustomResponse.builder().ketQua(giangVienResponse).loiNhan("Them sinh vien thanh cong").build();
	}
}
