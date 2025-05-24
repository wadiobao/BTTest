package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.GiangVien;
import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.entity.MonHoc;
import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.khoa.KhoaRequest;
import com.baitap.quanlisinhvien.model.khoa.KhoaResponse;
import com.baitap.quanlisinhvien.repository.KhoaRepository;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class KhoaService {
	KhoaRepository khoaRepository;

	public CustomResponse<Object> hienThiTatCaKhoa() {
		List<Khoa> danhSachKhoa = khoaRepository.findAll();
		List<KhoaResponse> danhKhoaResponses = new ArrayList<KhoaResponse>();
		for (Khoa khoa : danhSachKhoa) {
			
			List<GiangVien> danhSachGiangVien = khoa.getDsGiangVien();
			Map<Long,String> danhSachGiangVienResponse = new HashMap<Long, String>();
			for (GiangVien giangVien : danhSachGiangVien) {
				danhSachGiangVienResponse.put(giangVien.getMaGiangVien(), giangVien.getTenGiangVien());
			}
			
			List<MonHoc> danhSachMonHoc = khoa.getDsMonHoc();
			Map<String,String> danhSachMonHocResponse = new HashMap<String, String>();
			for (MonHoc monHoc : danhSachMonHoc) {
				danhSachMonHocResponse.put(monHoc.getMaMonHoc(),monHoc.getTenMonHoc());
			}
			
			List<SinhVien> danhSachSinhVien = khoa.getDsSinhVien();
			Map<Long,String> danhSachSinhVienResponse = new HashMap<Long, String>();
			for (SinhVien sinhVien : danhSachSinhVien) {
				danhSachSinhVienResponse.put(sinhVien.getMaSinhVien(),sinhVien.getHoTen());
			}
			
			KhoaResponse khoaResponse = KhoaResponse.builder()
					.maKhoa(khoa.getMaKhoa())
					.tenKhoa(khoa.getTenKhoa())
					.dsGiangVien(danhSachGiangVienResponse)
					.dsMonHoc(danhSachMonHocResponse)
					.dsSinhVien(danhSachSinhVienResponse)
					.build();
			
			danhKhoaResponses.add(khoaResponse);
		}
		return CustomResponse.builder().ketQua(danhKhoaResponses).loiNhan("Hien thi tat ca khoa").build();
	}

	public CustomResponse<Object> themKhoa(KhoaRequest khoaRequest) {
		if (khoaRepository.existsByTenKhoa(khoaRequest.getTenKhoa()))
			throw new RuntimeException("Da ton tai ten khoa");
		else if (khoaRepository.existsById(khoaRequest.getMaKhoa()))
			throw new RuntimeException("Da ton tai ma khoa");

		Khoa khoaMoi = Khoa.builder().maKhoa(khoaRequest.getMaKhoa()).tenKhoa(khoaRequest.getTenKhoa())
				.dsGiangVien(new ArrayList<>()).dsMonHoc(new ArrayList<>()).build();

		khoaRepository.save(khoaMoi);

		return CustomResponse.builder().ketQua(khoaMoi).loiNhan("Them khoa moi thanh cong").build();
	}
}
