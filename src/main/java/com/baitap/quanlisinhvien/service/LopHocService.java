package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.hibernate.Hibernate;
import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.LopHoc;
import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.lophoc.LopHocRequest;
import com.baitap.quanlisinhvien.model.lophoc.LopHocResponse;
import com.baitap.quanlisinhvien.repository.LopHocRepository;
import com.baitap.quanlisinhvien.repository.SinhVienRepository;

import jakarta.transaction.Transactional;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;

@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class LopHocService {
	LopHocRepository lopHocRepository;
	SinhVienRepository sinhVienRepository;

	public CustomResponse<Object> hienThiTatCaLopHoc() {
		List<LopHoc> danhSachLopHoc = lopHocRepository.findAll();
		
		
		List<LopHocResponse> danhSachLopHocResponses = new ArrayList<LopHocResponse>();
		
		for (LopHoc lopHoc : danhSachLopHoc) {
			
			Map<Long,String> dsSinhVien = new HashMap<Long, String>();
			for (SinhVien sinhVien : lopHoc.getDsSinhVien()) {
				dsSinhVien.put(sinhVien.getMaSinhVien(), sinhVien.getHoTen());
			}
			
			LopHocResponse lopHocResponse = LopHocResponse.builder()
					.maLop(lopHoc.getMaLop())
					.tenLop(lopHoc.getTenLop())
					.phong(lopHoc.getPhong())
					.tietBatDau(lopHoc.getTietBatDau())
					.tietKetThuc(lopHoc.getTietKetThuc())
					.ngayBatDau(lopHoc.getNgayBatDau())
					.ngayKetThuc(lopHoc.getNgayKetThuc())
					.siSo(lopHoc.getSiSo())
					.dsSinhVien(dsSinhVien)
					.build();
			
			danhSachLopHocResponses.add(lopHocResponse);

		}
		
		
		return CustomResponse.builder().ketQua(danhSachLopHocResponses).loiNhan("Hien thi tat ca lop hoc").build();
	}

	public CustomResponse<Object> themLopHoc(LopHocRequest lopHocRequest) {
		
		if(lopHocRepository.existsById(lopHocRequest.getMaLop()))
			throw new RuntimeException("Ma lop da ton tai");

		if(lopHocRequest.getTietBatDau()>lopHocRequest.getTietKetThuc())
			throw new RuntimeException("Tiet ket thuc phai lon hon tiet bat dau");
		
		
		LopHoc lopHocMoi = LopHoc.builder()
				.maLop(lopHocRequest.getMaLop())
				.tenLop(lopHocRequest.getTenLop())
				.phong(lopHocRequest.getPhong())
				.tietBatDau(lopHocRequest.getTietBatDau())
				.tietKetThuc(lopHocRequest.getTietKetThuc())
				.ngayBatDau(lopHocRequest.getNgayBatDau())
				.ngayKetThuc(lopHocRequest.getNgayKetThuc())
				.siSo(lopHocRequest.getSiSo())
				.dsSinhVien(new ArrayList<>())
				.build();

		lopHocRepository.save(lopHocMoi);

		return CustomResponse.builder().ketQua(lopHocMoi).loiNhan("Them lop hoc moi thanh cong").build();
	}
	
	public CustomResponse<Object> xoaLopHoc(String id) {

		LopHoc lopHoc = lopHocRepository.findById(id).orElseThrow(() -> new RuntimeException("Khong ton tai lop hoc"));
		Map<Long,String> dsSinhVien = new HashMap<Long, String>();
		for (SinhVien sinhVien : lopHoc.getDsSinhVien()) {
			dsSinhVien.put(sinhVien.getMaSinhVien(), sinhVien.getHoTen());
		}
		
		lopHocRepository.delete(lopHoc);
		
		LopHocResponse lopHocResponse = LopHocResponse.builder()
				.maLop(id)
				.tenLop(lopHoc.getTenLop())
				.phong(lopHoc.getPhong())
				.tietBatDau(lopHoc.getTietBatDau())
				.tietKetThuc(lopHoc.getTietKetThuc())
				.ngayBatDau(lopHoc.getNgayBatDau())
				.ngayKetThuc(lopHoc.getNgayKetThuc())
				.siSo(lopHoc.getSiSo())
				.dsSinhVien(dsSinhVien)
				.build();

		return CustomResponse.builder().ketQua(lopHocResponse).loiNhan("Xoa lop hoc moi thanh cong").build();
	}
	
	@Transactional
	public CustomResponse<Object> suaLopHoc(String id, LopHocRequest lopHocRequest) {
		if(lopHocRequest.getTietBatDau()>lopHocRequest.getTietKetThuc())
			throw new RuntimeException("Tiet ket thuc phai lon hon tiet bat dau");
		
		LopHoc lopHoc = lopHocRepository.findById(id).orElseThrow(() -> new RuntimeException("Khong ton tai lop hoc"));
	
		Hibernate.initialize(lopHoc.getDsSinhVien());
		
		List<SinhVien> dsSinhVien = lopHoc.getDsSinhVien();
		dsSinhVien.clear();
		
		for (Map.Entry<Long, String> tenSinhVien : lopHocRequest.getDsSinhVien().entrySet()) {
			SinhVien sinhVien = sinhVienRepository.findById(tenSinhVien.getKey()).orElseThrow();
			dsSinhVien.add(sinhVien);
		}
		
		lopHoc.setTenLop(lopHocRequest.getTenLop());
		lopHoc.setPhong(lopHocRequest.getPhong());
		lopHoc.setTietBatDau(lopHocRequest.getTietBatDau());
		lopHoc.setTietKetThuc(lopHocRequest.getTietKetThuc());
		lopHoc.setNgayBatDau(lopHocRequest.getNgayBatDau());
		lopHoc.setNgayKetThuc(lopHocRequest.getNgayKetThuc());
		lopHoc.setSiSo(lopHocRequest.getSiSo());
		lopHoc.setDsSinhVien(dsSinhVien);;
		
		lopHocRepository.save(lopHoc);
		
		LopHocResponse lopHocResponse = LopHocResponse.builder()
				.maLop(id)
				.tenLop(lopHoc.getTenLop())
				.phong(lopHoc.getPhong())
				.tietBatDau(lopHoc.getTietBatDau())
				.tietKetThuc(lopHoc.getTietKetThuc())
				.ngayBatDau(lopHoc.getNgayBatDau())
				.ngayKetThuc(lopHoc.getNgayKetThuc())
				.siSo(lopHoc.getSiSo())
				.dsSinhVien(lopHocRequest.getDsSinhVien())
				.build();
		
		return CustomResponse.builder().ketQua(lopHocResponse).loiNhan("Sua lop hoc moi thanh cong").build();

		
	}
}
