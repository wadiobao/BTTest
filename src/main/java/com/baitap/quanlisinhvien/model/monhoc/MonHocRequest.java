package com.baitap.quanlisinhvien.model.monhoc;

import java.util.List;

import com.baitap.quanlisinhvien.entity.Khoa;
import com.baitap.quanlisinhvien.entity.SinhVien;
import com.baitap.quanlisinhvien.model.khoa.KhoaResponse;

import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.validation.constraints.Size;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.FieldDefaults;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@FieldDefaults(level = AccessLevel.PRIVATE)
public class MonHocRequest {
	String maMonHoc;
	String tenMonHoc;
	String tenKhoa;
}
