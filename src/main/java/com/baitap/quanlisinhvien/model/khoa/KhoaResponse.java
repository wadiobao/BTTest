package com.baitap.quanlisinhvien.model.khoa;



import java.util.List;
import java.util.Map;

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
public class KhoaResponse {
	String maKhoa;
	String tenKhoa;
	Map<String,String> dsMonHoc;
	Map<Long,String> dsGiangVien;
	Map<Long,String> dsSinhVien;
}
