package com.baitap.quanlisinhvien.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.enums.ErrorCode;
import com.baitap.quanlisinhvien.exception.ExceptionHandle;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.SinhVienRequest;
import com.baitap.quanlisinhvien.model.SinhVienResponse;
import com.baitap.quanlisinhvien.repository.SinhVienRepository;

import jakarta.transaction.Transactional;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;


@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class SinhVienService {
	SinhVienRepository sinhVienRepository;

	public CustomResponse<Object> hienThiTatCaSinhVien() {
		List<SinhVien> danhSanhSinhVien = sinhVienRepository.findAll();
		return CustomResponse.builder().ketQua(danhSanhSinhVien).loiNhan("Hien thi tat ca sinh vien").build();
	}

	public CustomResponse<Object> hienThiThongTinSinhVienTheoId(String id) {
		SinhVien sinhVien = sinhVienRepository.findById(id)
				.orElseThrow(() -> new ExceptionHandle(ErrorCode.KHONG_TIM_THAY));


		return CustomResponse.builder().ketQua(sinhVien).loiNhan("Hien thi thong tin sinh vien").build();
	}

	public CustomResponse<Object> hienThiThongTinCacSinhVienTheoTen(String hoTen) {
		
		List<SinhVien> danhSachSinhVien = sinhVienRepository.findAllByHoTenContainingIgnoreCase(hoTen).orElseThrow();
		if (danhSachSinhVien.isEmpty())
			throw new ExceptionHandle(ErrorCode.KHONG_TIM_THAY);
		
		return CustomResponse.builder().ketQua(danhSachSinhVien)
				.loiNhan("Hien thi thong tin sinh vien theo ten can tim").build();
	}

	public CustomResponse<Object> themSinhVien(SinhVienRequest sinhVienRequest) {

		SinhVien sinhVien = SinhVien.builder().hoTen(sinhVienRequest.getHoTen()).ngaySinh(sinhVienRequest.getNgaySinh())
				.email(sinhVienRequest.getEmail()).diaChi(sinhVienRequest.getDiaChi()).sdt(sinhVienRequest.getSdt())
				.build();

		sinhVienRepository.save(sinhVien);

		return CustomResponse.builder()
				.ketQua(SinhVienResponse.builder().hoTen(sinhVienRequest.getHoTen())
						.ngaySinh(sinhVienRequest.getNgaySinh()).email(sinhVienRequest.getEmail())
						.diaChi(sinhVienRequest.getDiaChi()).sdt(sinhVienRequest.getSdt()).build())
				.loiNhan("Them sinh vien thanh cong").build();
	}

	@Transactional
	public CustomResponse<Object> suaThongTinSinhVien(String id, SinhVienRequest sinhVienRequest) {
		SinhVien sinhVien;
		if (!sinhVienRepository.existsById(id))
			return CustomResponse.builder().loiNhan("Khong tim thay sinh vien").build();
		sinhVien = sinhVienRepository.findById(id).orElseThrow();

		sinhVien.setHoTen(sinhVienRequest.getHoTen());
		sinhVien.setDiaChi(sinhVienRequest.getDiaChi());
		sinhVien.setEmail(sinhVienRequest.getEmail());
		sinhVien.setNgaySinh(sinhVienRequest.getNgaySinh());
		sinhVien.setSdt(sinhVienRequest.getSdt());

		sinhVienRepository.save(sinhVien);

		return CustomResponse.builder()
				.ketQua(SinhVienResponse.builder().hoTen(sinhVienRequest.getHoTen())
						.ngaySinh(sinhVienRequest.getNgaySinh()).email(sinhVienRequest.getEmail())
						.diaChi(sinhVienRequest.getDiaChi()).sdt(sinhVienRequest.getSdt()).build())
				.loiNhan("Sua thong tin sinh vien thanh cong").build();
	}

	public CustomResponse<Object> xoaSinhVien(String id) {
		SinhVien sinhVien;
		if (!sinhVienRepository.existsById(id))
			return CustomResponse.builder().loiNhan("Khong tim thay sinh vien").build();
		sinhVien = sinhVienRepository.findById(id).orElseThrow();
		sinhVienRepository.delete(sinhVien);

		return CustomResponse.builder()
				.ketQua(SinhVienResponse.builder().hoTen(sinhVien.getHoTen()).ngaySinh(sinhVien.getNgaySinh())
						.email(sinhVien.getEmail()).diaChi(sinhVien.getDiaChi()).sdt(sinhVien.getSdt()).build())
				.loiNhan("Sua thong tin sinh vien thanh cong").build();
	}

}
