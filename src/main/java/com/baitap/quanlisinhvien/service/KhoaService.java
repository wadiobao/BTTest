package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.hibernate.Hibernate;
import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.GiangVien;
import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.entity.MonHoc;
import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.enums.ErrorCode;
import com.baitap.quanlisinhvien.exception.ExceptionHandle;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.khoa.KhoaRequest;
import com.baitap.quanlisinhvien.model.khoa.KhoaResponse;
import com.baitap.quanlisinhvien.repository.GiangVienRepository;
import com.baitap.quanlisinhvien.repository.KhoaRepository;
import com.baitap.quanlisinhvien.repository.MonHocRepository;
import com.baitap.quanlisinhvien.repository.SinhVienRepository;

import jakarta.transaction.Transactional;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class KhoaService {
	KhoaRepository khoaRepository;
	MonHocRepository monHocRepository;
	GiangVienRepository giangVienRepository;
	SinhVienRepository sinhVienRepository;

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
	
	@Transactional
	public CustomResponse<Object> suaKhoa(String id,KhoaRequest khoaRequest) {
		Khoa khoa = khoaRepository.findById(id).orElseThrow(() -> new ExceptionHandle(ErrorCode.KHOA_KHONG_TON_TAI));

		List<MonHoc> dsMonHoc = new ArrayList<MonHoc>();
		List<GiangVien> dsGiangVien = new ArrayList<GiangVien>();
		List<SinhVien> dsSinhVien = new ArrayList<SinhVien>();
		
		for (Map.Entry<String, String> mapMonHoc : khoaRequest.getDsMonHoc().entrySet()) {
			MonHoc monHoc = monHocRepository.findById(mapMonHoc.getKey()).orElseThrow();
			dsMonHoc.add(monHoc);
		}
		
		for (Map.Entry<Long, String> mapGiangVien : khoaRequest.getDsGiangVien().entrySet()) {
			GiangVien giangVien = giangVienRepository.findById(mapGiangVien.getKey()).orElseThrow();
			dsGiangVien.add(giangVien);
		}
		
		for (Map.Entry<Long, String> mapSinhVien : khoaRequest.getDsSinhVien().entrySet()) {
			SinhVien sinhVien = sinhVienRepository.findById(mapSinhVien.getKey()).orElseThrow();
			dsSinhVien.add(sinhVien);
		}
		
		List<GiangVien> giangVienCu = khoa.getDsGiangVien();
		giangVienCu.clear();
		giangVienCu.addAll(dsGiangVien); 
		
		List<MonHoc> monHocCu = khoa.getDsMonHoc();
		monHocCu.clear(); 
		monHocCu.addAll(dsMonHoc); 
		
		List<SinhVien> sinhVienCu = khoa.getDsSinhVien();
		sinhVienCu.clear(); 
		sinhVienCu.addAll(dsSinhVien);

		
		khoa.setTenKhoa(khoaRequest.getTenKhoa());
		khoa.setDsMonHoc(monHocCu);
		khoa.setDsGiangVien(giangVienCu);
		khoa.setDsSinhVien(sinhVienCu);
		
		khoaRepository.save(khoa);
		
		KhoaResponse khoaResponse = KhoaResponse.builder()
				.maKhoa(khoa.getMaKhoa())
				.tenKhoa(khoa.getTenKhoa())
				.dsGiangVien(khoaRequest.getDsGiangVien())
				.dsMonHoc(khoaRequest.getDsMonHoc())
				.dsSinhVien(khoaRequest.getDsSinhVien())
				.build();
		
		return CustomResponse.builder().ketQua(khoaResponse).loiNhan("Sua khoa thanh cong").build();

	}
		
	
	public CustomResponse<Object> xoaKhoa(String id) {
		Khoa khoa = khoaRepository.findById(id).orElseThrow(() -> new ExceptionHandle(ErrorCode.KHOA_KHONG_TON_TAI));

		khoaRepository.delete(khoa);
		
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

		return CustomResponse.builder().ketQua(khoaResponse).loiNhan("Xoa khoa thanh cong").build();
	}
	
	
}
