package TestBT2;

import java.util.Scanner;

public class PhanSo {
	private int tuSo;
	private int mauSo;

	public PhanSo() {
	}

	public PhanSo(int tuSo, int mauSo) {
		this.tuSo = tuSo;
		this.mauSo = mauSo;
	}

	public int getTuSo() {
		return tuSo;
	}

	public void setTuSo(int tuSo) {
		this.tuSo = tuSo;
	}

	public int getMauSo() {
		return mauSo;
	}

	public void setMauSo(int mauSo) {
		this.mauSo = mauSo;
	}

	public PhanSo congHaiPhanSo(PhanSo ps) {
		PhanSo tong = new PhanSo();
		int tuSoTong = ps.getMauSo() * tuSo + mauSo * ps.getTuSo();
		int mauSoTong = ps.getMauSo() * mauSo;
		int ucln = UCLN(tuSoTong, mauSoTong);
		tong.setMauSo(mauSoTong / ucln);
		tong.setTuSo(tuSoTong / ucln);

		return tong;
	}

	public PhanSo truHaiPhanSo(PhanSo ps) {
		PhanSo hieu = new PhanSo();
		int tuSoHieu = ps.getMauSo() * tuSo - mauSo * ps.getTuSo();
		int mauSoHieu = ps.getMauSo() * mauSo;
		int ucln = UCLN(tuSoHieu, mauSoHieu);
		hieu.setMauSo(mauSoHieu / ucln);
		hieu.setTuSo(tuSoHieu / ucln);
		return hieu;
	}

	public PhanSo nhanHaiPhanSo(PhanSo ps) {
		PhanSo tich = new PhanSo();
		int tuSoTich = ps.getTuSo() * tuSo;
		int mauSoTich = ps.getMauSo() * mauSo;
		int ucln = UCLN(tuSoTich, mauSoTich);
		tich.setMauSo(mauSoTich / ucln);
		tich.setTuSo(tuSoTich / ucln);
		return tich;
	}

	public PhanSo chiaHaiPhanSo(PhanSo ps) {
		PhanSo thuong = new PhanSo();
		int tuSoThuong = tuSo * ps.getMauSo();
		int mauSoThuong = mauSo * ps.getTuSo();
		int ucln = UCLN(tuSoThuong, mauSoThuong);
		thuong.setMauSo(mauSoThuong / ucln);
		thuong.setTuSo(tuSoThuong / ucln);
		return thuong;
	}

	private int UCLN(int a, int b) {
		while (b != 0) {
			int r = a % b;
			a = b;
			b = r;
		}

		return a;
	}

	@Override
	public String toString() {
		return tuSo + "/" + mauSo;
	}

	public static void main(String[] args) {
		int tuSo, mauSo;
		Scanner sc = new Scanner(System.in);
		System.out.println("Nhap tu so va mau so phan so 1: ");
		tuSo = sc.nextInt();
		mauSo = sc.nextInt();

		PhanSo phanSoA = new PhanSo(tuSo, mauSo);

		System.out.println("Nhap tu so va mau so phan so 2: ");
		tuSo = sc.nextInt();
		mauSo = sc.nextInt();

		PhanSo phanSoB = new PhanSo(tuSo, mauSo);

		PhanSo tong = phanSoA.congHaiPhanSo(phanSoB);
		System.out.println("Tong hai phan so la: " + tong.toString());

		PhanSo hieu = phanSoA.truHaiPhanSo(phanSoB);
		System.out.println("Hieu hai phan so la: " + hieu.toString());

		PhanSo tich = phanSoA.nhanHaiPhanSo(phanSoB);
		System.out.println("Tich hai phan so la: " + tich.toString());

		PhanSo thuong = phanSoA.chiaHaiPhanSo(phanSoB);
		System.out.println("Thuong hai phan so la: " + thuong.toString());

		sc.close();
	}
}
