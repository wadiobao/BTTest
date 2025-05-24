package com.baitap.quanlisinhvien.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.entity.MonHoc;
import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.enums.ErrorCode;
import com.baitap.quanlisinhvien.exception.ExceptionHandle;
import com.baitap.quanlisinhvien.model.CustomResponse;
import com.baitap.quanlisinhvien.model.sinhvien.SinhVienRequest;
import com.baitap.quanlisinhvien.model.sinhvien.SinhVienResponse;
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
public class SinhVienService {
	SinhVienRepository sinhVienRepository;
	
	KhoaRepository khoaRepository;
	
	MonHocRepository monHocRepository;

	public CustomResponse<Object> hienThiTatCaSinhVien() {
		List<SinhVien> danhSanhSinhVien = sinhVienRepository.findAll();
		List<SinhVienResponse> danhSanhSinhVienResponses = new ArrayList<SinhVienResponse>();

		for (SinhVien sinhVien : danhSanhSinhVien) {
	
			SinhVienResponse sinhVienResponse = SinhVienResponse.builder()
					.hoTen(sinhVien.getHoTen())
					.gioiTinh(sinhVien.getGioiTinh())
					.ngaySinh(sinhVien.getNgaySinh())
					.email(sinhVien.getEmail())
					.diaChi(sinhVien.getDiaChi())
					.sdt(sinhVien.getSdt())
					.tenKhoa(sinhVien.getKhoa().getTenKhoa())
					.diem(sinhVien.getDiemMonHoc())
					.build();

			danhSanhSinhVienResponses.add(sinhVienResponse);
		}
		return CustomResponse.builder().ketQua(danhSanhSinhVienResponses).loiNhan("Hien thi tat ca sinh vien").build();
	}

	public CustomResponse<Object> hienThiThongTinSinhVienTheoId(Long id) {
		SinhVien sinhVien = sinhVienRepository.findById(id)
				.orElseThrow(() -> new ExceptionHandle(ErrorCode.KHONG_TIM_THAY));
		
		
		SinhVienResponse sinhVienResponse = SinhVienResponse.builder()
				.hoTen(sinhVien.getHoTen())
				.gioiTinh(sinhVien.getGioiTinh())
				.ngaySinh(sinhVien.getNgaySinh())
				.email(sinhVien.getEmail())
				.diaChi(sinhVien.getDiaChi())
				.sdt(sinhVien.getSdt())
				.diem(sinhVien.getDiemMonHoc())
				.tenKhoa(sinhVien.getKhoa().getTenKhoa())
				.build();

		return CustomResponse.builder().ketQua(sinhVienResponse).loiNhan("Hien thi thong tin sinh vien").build();
	}

	public CustomResponse<Object> hienThiThongTinCacSinhVienTheoTen(String hoTen) {
		
		List<SinhVien> danhSachSinhVien = sinhVienRepository.findAllByHoTenContainingIgnoreCase(hoTen).orElseThrow();

		if (danhSachSinhVien.isEmpty())
			throw new ExceptionHandle(ErrorCode.KHONG_TIM_THAY);
		
		List<SinhVienResponse> danhSachSinhVienResponses = new ArrayList<SinhVienResponse>();
		
		for (SinhVien sinhVien : danhSachSinhVien) {
			SinhVienResponse sinhVienResponse = SinhVienResponse.builder()
					.hoTen(sinhVien.getHoTen())
					.gioiTinh(sinhVien.getGioiTinh())
					.ngaySinh(sinhVien.getNgaySinh())
					.email(sinhVien.getEmail())
					.diaChi(sinhVien.getDiaChi())
					.sdt(sinhVien.getSdt())
					.diem(sinhVien.getDiemMonHoc())
					.tenKhoa(sinhVien.getKhoa().getTenKhoa())
					.build();
			
			danhSachSinhVienResponses.add(sinhVienResponse);
		}
		
		return CustomResponse.builder().ketQua(danhSachSinhVienResponses)
				.loiNhan("Hien thi thong tin sinh vien theo ten can tim").build();
	}
	
public CustomResponse<Object> hienThiThongTinCacSinhVienTheoTenPhanTrang(String hoTen, int page, int size, String sortBy, String direction) {
	
		Sort sort;
		if(direction.equalsIgnoreCase("desc")) {
			sort = Sort.by(sortBy).descending();
		}else {
			sort = Sort.by(sortBy).ascending();
		}
		
		Pageable pageable = PageRequest.of(page, size, sort);
		
		Page<SinhVien> pageSinhVien = sinhVienRepository.findAllByHoTenContainingIgnoreCase(hoTen, pageable);

		if (pageSinhVien.isEmpty())
			throw new ExceptionHandle(ErrorCode.KHONG_TIM_THAY);
		
		List<SinhVienResponse> danhSachSinhVienResponses = pageSinhVien
			    .map(sv -> SinhVienResponse.builder()
			        .hoTen(sv.getHoTen())
			        .gioiTinh(sv.getGioiTinh())
			        .ngaySinh(sv.getNgaySinh())
			        .email(sv.getEmail())
			        .diaChi(sv.getDiaChi())
			        .sdt(sv.getSdt())
			        .diem(sv.getDiemMonHoc())
			        .tenKhoa(sv.getKhoa().getTenKhoa())
			        .build()
			    ).getContent();
		
		return CustomResponse.builder().ketQua(danhSachSinhVienResponses)
				.loiNhan("Hien thi thong tin sinh vien theo ten can tim").build();
	}

	public CustomResponse<Object> themSinhVien(SinhVienRequest sinhVienRequest) {
		
		Khoa khoa = khoaRepository.findByTenKhoa(sinhVienRequest.getTenKhoa())
				.orElseThrow(() -> new ExceptionHandle(ErrorCode.KHOA_KHONG_TON_TAI));
		

		SinhVien sinhVien = SinhVien.builder()
				.hoTen(sinhVienRequest.getHoTen())
				.gioiTinh(sinhVienRequest.getGioiTinh())
				.ngaySinh(sinhVienRequest.getNgaySinh())
				.email(sinhVienRequest.getEmail())
				.diaChi(sinhVienRequest.getDiaChi())
				.sdt(sinhVienRequest.getSdt())
				.khoa(khoa)
				.build();

		sinhVienRepository.save(sinhVien);

		return CustomResponse.builder()
				.ketQua(SinhVienResponse.builder()
						.hoTen(sinhVienRequest.getHoTen())
						.gioiTinh(sinhVienRequest.getGioiTinh())
						.ngaySinh(sinhVienRequest.getNgaySinh())
						.email(sinhVienRequest.getEmail())
						.diaChi(sinhVienRequest.getDiaChi())
						.sdt(sinhVienRequest.getSdt())
						.tenKhoa(khoa.getTenKhoa())
						.build())
				.loiNhan("Them sinh vien thanh cong").build();
	}

	@Transactional
	public CustomResponse<Object> suaThongTinSinhVien(Long id, SinhVienRequest sinhVienRequest) {
		SinhVien sinhVien;
		if (!sinhVienRepository.existsById(id))
			return CustomResponse.builder().loiNhan("Khong tim thay sinh vien").build();
		sinhVien = sinhVienRepository.findById(id).orElseThrow();
		
		Khoa khoa = khoaRepository.findByTenKhoa(sinhVienRequest.getTenKhoa())
				.orElseThrow(() -> new ExceptionHandle(ErrorCode.KHOA_KHONG_TON_TAI));
		
		List<MonHoc> monHocTrongKhoa = khoa.getDsMonHoc();
		
		Set<String> dsTenMonDaHoc = sinhVienRequest.getDiem().keySet();
		Map<String, Float> diemMonHoc = new HashMap<String, Float>();
		List<MonHoc> monDaHoc = new ArrayList<MonHoc>();
		for (String tenMonHoc : dsTenMonDaHoc) {
			MonHoc monHoc = monHocRepository.findByTenMonHoc(tenMonHoc)
					.orElseThrow(() -> new RuntimeException("Mon hoc "+tenMonHoc+" khong ton tai"));
			
			if(!monHocTrongKhoa.contains(monHoc)) throw new RuntimeException("Mon hoc "+tenMonHoc+" khong ton tai trong khoa "+khoa.getTenKhoa());
			
			diemMonHoc.put(tenMonHoc,sinhVienRequest.getDiem().get(tenMonHoc));
			monDaHoc.add(monHoc);
		}
		
		sinhVien.setHoTen(sinhVienRequest.getHoTen());
		sinhVien.setDiaChi(sinhVienRequest.getDiaChi());
		sinhVien.setEmail(sinhVienRequest.getEmail());
		sinhVien.setNgaySinh(sinhVienRequest.getNgaySinh());
		sinhVien.setSdt(sinhVienRequest.getSdt());
		sinhVien.setKhoa(khoa);
		sinhVien.setDiemMonHoc(diemMonHoc);

		sinhVienRepository.save(sinhVien);

		return CustomResponse.builder()
				.ketQua(SinhVienResponse.builder()
						.hoTen(sinhVienRequest.getHoTen())
						.gioiTinh(sinhVienRequest.getGioiTinh())
						.ngaySinh(sinhVienRequest.getNgaySinh())
						.email(sinhVienRequest.getEmail())
						.diaChi(sinhVienRequest.getDiaChi())
						.sdt(sinhVienRequest.getSdt())
						.tenKhoa(khoa.getTenKhoa())
						.diem(diemMonHoc)
						.build())
				.loiNhan("Sua thong tin sinh vien thanh cong").build();
	}

	public CustomResponse<Object> xoaSinhVien(Long id) {
		SinhVien sinhVien;
		if (!sinhVienRepository.existsById(id))
			return CustomResponse.builder().loiNhan("Khong tim thay sinh vien").build();
		sinhVien = sinhVienRepository.findById(id).orElseThrow();
		sinhVienRepository.delete(sinhVien);

		return CustomResponse.builder()
				.ketQua(SinhVienResponse.builder().hoTen(sinhVien.getHoTen()).ngaySinh(sinhVien.getNgaySinh())
						.email(sinhVien.getEmail()).diaChi(sinhVien.getDiaChi()).sdt(sinhVien.getSdt()).build())
				.loiNhan("Xoa sinh vien thanh cong").build();
	}

}
