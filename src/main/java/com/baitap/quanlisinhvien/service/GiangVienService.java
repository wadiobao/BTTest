package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.GiangVien;
import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.entity.MonHoc;
import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.enums.ErrorCode;
import com.baitap.quanlisinhvien.exception.ExceptionHandle;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.giangvien.GiangVienRequest;
import com.baitap.quanlisinhvien.model.giangvien.GiangVienResponse;
import com.baitap.quanlisinhvien.model.sinhvien.SinhVienResponse;
import com.baitap.quanlisinhvien.repository.GiangVienRepository;
import com.baitap.quanlisinhvien.repository.KhoaRepository;

import jakarta.transaction.Transactional;
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
	
	@Transactional
	public CustomResponse<Object> suaGiangVien(Long id, GiangVienRequest giangVienRequest){
		GiangVien giangVien;
		if (!giangVienRepository.existsById(id))
			return CustomResponse.builder().loiNhan("Khong tim thay giang vien").build();
		
		giangVien = giangVienRepository.findById(id).orElseThrow();
		
		Khoa khoa = khoaRepository.findByTenKhoa(giangVienRequest.getTenKhoa())
				.orElseThrow(() -> new ExceptionHandle(ErrorCode.KHOA_KHONG_TON_TAI));
		
		
		giangVien.setTenGiangVien(giangVienRequest.getTenGiangVien());
		giangVien.setGioiTinh(giangVienRequest.getGioiTinh());
		giangVien.setDiaChi(giangVienRequest.getDiaChi());
		giangVien.setEmail(giangVienRequest.getEmail());
		giangVien.setNgaySinh(giangVienRequest.getNgaySinh());
		giangVien.setSdt(giangVienRequest.getSdt());
		giangVien.setKhoa(khoa);

		giangVienRepository.save(giangVien);

		return CustomResponse.builder()
				.ketQua(GiangVienResponse.builder()
						.tenGiangVien(giangVienRequest.getTenGiangVien())
						.gioiTinh(giangVienRequest.getGioiTinh())
						.ngaySinh(giangVienRequest.getNgaySinh())
						.email(giangVienRequest.getEmail())
						.diaChi(giangVienRequest.getDiaChi())
						.sdt(giangVienRequest.getSdt())
						.tenKhoa(khoa.getTenKhoa())
						.build())
				.loiNhan("Sua thong tin giang vien thanh cong").build();
	}
	
	public CustomResponse<Object> xoaGiangVien(Long id) {
		GiangVien giangVien;
		if (!giangVienRepository.existsById(id))
			return CustomResponse.builder().loiNhan("Khong tim thay giang vien").build();
		giangVien = giangVienRepository.findById(id).orElseThrow();
		giangVienRepository.delete(giangVien);
		
		GiangVienResponse giangVienResponse = GiangVienResponse.builder()
				.tenGiangVien(giangVien.getTenGiangVien())
				.gioiTinh(giangVien.getGioiTinh())
				.ngaySinh(giangVien.getNgaySinh())
				.email(giangVien.getEmail())
				.diaChi(giangVien.getDiaChi())
				.sdt(giangVien.getSdt())
				.tenKhoa(giangVien.getKhoa().getTenKhoa())
				.build();

		return CustomResponse.builder()
				.ketQua(giangVienResponse)
				.loiNhan("Xoa giang vien thanh cong").build();
	}
}
