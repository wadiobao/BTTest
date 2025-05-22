package TestBT2;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.SortedSet;
import java.util.stream.Collectors;

public class SinhVien {
	private String id;
	private String name;
	private String address;
	private int age;
	private float gpa;

	public SinhVien() {

	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public float getGpa() {
		return gpa;
	}

	public void setGpa(float gpa) {
		this.gpa = gpa;
	}

	public SinhVien themSinhVien(Scanner sc) {

		System.out.println("Nhap ma sinh vien: ");
		id = sc.nextLine();

		System.out.println("Nhap ten sinh vien: ");
		name = sc.nextLine();

		System.out.println("Nhap dia chi sinh vien: ");
		address = sc.nextLine();

		System.out.println("Nhap tuoi sinh vien: ");
		age = sc.nextInt();

		System.out.println("Nhap gpa cua sinh vien: ");
		gpa = sc.nextFloat();

		return this;
	}

	public static void chinhSuaThongTinTheoId(ArrayList<SinhVien> danhSanhSinhVien, String id, Scanner sc) {

		for (SinhVien sinhVien : danhSanhSinhVien) {
			if (sinhVien.getId().equals(id)) {
				int chon;
				System.out.println("Tim thay sinh vien co id " + id);
				System.out.println(sinhVien.toString());
				do {
					sinhVien.toString();
					System.out.println("Chon thong tin muon thay doi: " + "\n" + "1. Ten sinh vien" + "\n"
							+ "2. Dia chi sinh vien" + "\n" + "3. Tuoi" + "\n" + "4. GPA" + "\n" + "5. Thoat");
					chon = sc.nextInt();
					sc.nextLine();
					switch (chon) {
					case 1:
						System.out.println("Nhap ten moi cua sinh vien:");
						sinhVien.setName(sc.nextLine());
						System.out.println("Thong tin sau khi thay doi");
						System.out.println(sinhVien.toString());
						break;
					case 2:
						System.out.println("Nhap dia chi moi cua sinh vien:");
						sinhVien.setAddress(sc.nextLine());
						System.out.println("Thong tin sau khi thay doi");
						System.out.println(sinhVien.toString());
						break;
					case 3:
						System.out.println("Nhap tuoi moi cua sinh vien:");
						sinhVien.setAge(sc.nextInt());
						System.out.println("Thong tin sau khi thay doi");
						System.out.println(sinhVien.toString());
						break;
					case 4:
						System.out.println("Nhap GPA moi cua sinh vien:");
						sinhVien.setGpa(sc.nextInt());
						System.out.println("Thong tin sau khi thay doi");
						System.out.println(sinhVien.toString());
						break;

					default:
						break;
					}
				} while (chon != 5);
				break;
			}
		}
		System.out.println("Khong tim thay sinh vien co id " + id);
	}

	public static void xoaSinhVienTheoId(ArrayList<SinhVien> danhSanhSinhVien, String id, Scanner sc) {
		for (SinhVien sinhVien : danhSanhSinhVien) {
			if (sinhVien.getId().equals(id)) {
				System.out.println("Tim thay sinh vien co id " + id);
				System.out.println(sinhVien.toString());
				System.out.println("Chac chan muon xoa \n" + "1. Co \n" + "2. khong \n");
				int chon = sc.nextInt();
				if (chon == 1) {
					danhSanhSinhVien.remove(sinhVien);
					System.out.println("Da xoa sinh vien co id " + id);
				}
				break;
			}
		}
		System.out.println("Khong tim thay sinh vien co id " + id);
	}

	public static ArrayList<SinhVien> sapXepSinhVienTheoGpa(ArrayList<SinhVien> danhSanhSinhVien, byte thuTu) {
		ArrayList<SinhVien> tmp = danhSanhSinhVien;
		Collections.sort(tmp, new Comparator<SinhVien>() {

			public int compare(SinhVien o1, SinhVien o2) {

				return (int) (Float.compare(o1.getGpa(), o2.getGpa()));
			}
		});
		if (thuTu == 1)
			Collections.reverse(tmp);

		return tmp;

	}

	public static ArrayList<SinhVien> sapXepSinhVienTheoTen(ArrayList<SinhVien> danhSanhSinhVien, byte thuTu) {
		ArrayList<SinhVien> tmp = danhSanhSinhVien;
		Collections.sort(tmp, new Comparator<SinhVien>() {

			public int compare(SinhVien o1, SinhVien o2) {

				return (int) (o1.getName().compareToIgnoreCase(o2.getName()));
			}
		});
		if (thuTu == 1)
			Collections.reverse(tmp);

		return tmp;

	}

	public static void hienThiDanhSachSinhVien(ArrayList<SinhVien> danhSanhSinhVien) {
		for (SinhVien sinhVien : danhSanhSinhVien) {
			System.out.println(sinhVien.toString());
		}
	}

	@Override
	public String toString() {
		return "Id=" + id + "\n" + "Ten=" + name + "\n" + "Dia chi=" + address + "\n" + "Tuoi=" + age + "\n" + "GPA="
				+ gpa + "\n";
	}

	public static void main(String[] args) {
		int nhap;
		Scanner sc = new Scanner(System.in);
		ArrayList<SinhVien> danhSanhSinhVien = new ArrayList<SinhVien>();
		do {
			System.out.println();
			System.out.println(" /****************************************/\r\n" + " 1. Add a student.\r\n"
					+ " 2. Edit student by id.\r\n" + " 3. Delete student by id.\r\n" + " 4. Sort students by gpa.\r\n"
					+ " 5. Sort students by name.\r\n" + " 6. Show students.\r\n" + " 0. Exit.\r\n"
					+ " /****************************************/");

			System.out.println("Nhap lua chon:");
			nhap = sc.nextInt();
			sc.nextLine();
			switch (nhap) {
			case 1:
				SinhVien sinhVien = new SinhVien();
				danhSanhSinhVien.add(sinhVien.themSinhVien(sc));
				break;
			case 2:
				System.out.println("Nhap id sinh vien muon sua: ");
				String idSua = sc.nextLine();
				chinhSuaThongTinTheoId(danhSanhSinhVien, idSua, sc);
				break;
			case 3:
				System.out.println("Nhap id sinh vien muon sua: ");
				String idXoa = sc.nextLine();
				xoaSinhVienTheoId(danhSanhSinhVien, idXoa, sc);
				break;
			case 4:
				System.out.println("Lua chon thu tu sap xep \n" + "0. Tang dan \n" + "1. Giam dan");
				byte thuTuGpa = sc.nextByte();
				danhSanhSinhVien = sapXepSinhVienTheoGpa(danhSanhSinhVien,thuTuGpa);

				System.out.println("Danh sach sinh vien sau khi sap xep theo gpa:");
				for (SinhVien sinhVienMoi : danhSanhSinhVien) {
					System.out.println(sinhVienMoi.toString());
				}
				break;
			case 5:
				System.out.println("Lua chon thu tu sap xep \n" + "0. Tang dan \n" + "1. Giam dan");
				byte thuTuTen = sc.nextByte();
				danhSanhSinhVien = sapXepSinhVienTheoTen(danhSanhSinhVien, thuTuTen);
				System.out.println("Danh sach sinh vien sau khi sap xep theo ten:");
				for (SinhVien sinhVienMoi : danhSanhSinhVien) {
					System.out.println(sinhVienMoi.toString());
				}
				break;
			case 6:
				System.out.println("Danh sach sinh vien: ");
				hienThiDanhSachSinhVien(danhSanhSinhVien);
				break;
			default:
				break;
			}
		} while (nhap != 0);

		sc.close();
		System.out.println("Da thoat chuong trinh");

	}

}
