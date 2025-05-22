import java.util.Scanner;

public class B2 {
	public static void main(String[] args) {
		int donGia, tieuThu, soDien;
		Scanner sc = new Scanner(System.in);
		System.out.println("Nhap so dien tieu thu:");
		tieuThu = sc.nextInt();

		if (tieuThu > 150)
			soDien = 1000 * 25 + 1250 * 50 + 75 * 1800 + (tieuThu - 150) * 2500;
		else if (tieuThu <= 150 && tieuThu > 75)
			soDien = 1000 * 25 + 1250 * 50 + (tieuThu - 75) * 1800;
		else if (tieuThu <= 75 && tieuThu > 25)
			soDien = 1000 * 25 + 1250 * (tieuThu - 25);
		else
			soDien = tieuThu * 1000;

		System.out.println("So dien phai tra la:" + soDien + "đ");
	}
}
