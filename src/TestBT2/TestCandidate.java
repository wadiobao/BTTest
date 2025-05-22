package TestBT2;

import java.util.ArrayList;
import java.util.Scanner;

public class TestCandidate {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		ArrayList<Candidate> danhSachThiSinh = new ArrayList<Candidate>();

		System.out.println("Nhap so thi sinh muon nhap:");
		int n = sc.nextInt();

		for (int i = 0; i < n; i++) {
			System.out.println("Nhap thong tin thi sinh so " + (i + 1));
			Candidate thiSinh = new Candidate();
			danhSachThiSinh.add(thiSinh.nhapThiSinh(sc));
		}

		System.out.println("Thong tin cac thi sinh co tong diem hon 1:");
		Candidate.hienThiThongTinThiSinhTongDiemHonMot(danhSachThiSinh);
		
		sc.close();
	}
}
