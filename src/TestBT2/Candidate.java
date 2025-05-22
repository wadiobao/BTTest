package TestBT2;

import java.util.ArrayList;

import java.util.Scanner;

public class Candidate {
	private int ma;
	private String ten;
	private String ngayThangNamSinh;
	private float diemToan;
	private float diemVan;
	private float diemAnh;

	public Candidate() {

	}

	public Candidate(int ma, String ten, String ngayThangNamSinh, float diemToan, float diemVan, float diemAnh) {
		this.ma = ma;
		this.ten = ten;
		this.ngayThangNamSinh = ngayThangNamSinh;
		this.diemToan = diemToan;
		this.diemVan = diemVan;
		this.diemAnh = diemAnh;
	}

	public int getMa() {
		return ma;
	}

	public void setMa(int ma) {
		this.ma = ma;
	}

	public String getTen() {
		return ten;
	}

	public void setTen(String ten) {
		this.ten = ten;
	}

	public String getNgayThangNamSinh() {
		return ngayThangNamSinh;
	}

	public void setNgayThangNamSinh(String ngayThangNamSinh) {
		this.ngayThangNamSinh = ngayThangNamSinh;
	}

	public float getDiemToan() {
		return diemToan;
	}

	public void setDiemToan(float diemToan) {
		this.diemToan = diemToan;
	}

	public float getDiemVan() {
		return diemVan;
	}

	public void setDiemVan(float diemVan) {
		this.diemVan = diemVan;
	}

	public float getDiemAnh() {
		return diemAnh;
	}

	public void setDiemAnh(float diemAnh) {
		this.diemAnh = diemAnh;
	}

	@Override
	public String toString() {
		return "Ma: " + ma + "\n" + "Ten: " + ten + "\n" + "Ngay thang nam sinh: " + ngayThangNamSinh + "\n"
				+ "Diem Toan: " + diemToan + "\n" + "Diem Van: " + diemVan + "\n" + "Diem Anh: " + diemAnh;
	}

	public Candidate nhapThiSinh(Scanner sc) {

		System.out.println("Nhap ma thi sinh: ");
		ma = sc.nextInt();
		sc.nextLine();
		System.out.println("Nhap ten thi sinh: ");
		ten = sc.nextLine();

		System.out.println("Nhap ngay thang nam sinh(dd/mm/yyyy): ");
		ngayThangNamSinh = sc.nextLine();

		do {
			System.out.println("Nhap diem Toan: ");
			diemToan = sc.nextFloat();
		} while (diemToan > 10 || diemToan < 0);

		do {
			System.out.println("Nhap diem Van: ");
			diemVan = sc.nextFloat();
		} while (diemVan > 10 || diemVan < 0);

		do {
			System.out.println("Nhap diem Anh: ");
			diemAnh = sc.nextFloat();
		} while (diemAnh > 10 || diemAnh < 0);

		return this;
	}

	public static void hienThiThongTinThiSinhTongDiemHonMot(ArrayList<Candidate> danhSachThiSinh) {
		for (Candidate thiSinh : danhSachThiSinh) {
			float tongDiem = thiSinh.getDiemToan() + thiSinh.getDiemVan() + thiSinh.getDiemAnh();
			if (tongDiem > 1)
				System.out.println(thiSinh.toString());
			System.out.println();
		}
	}

}
