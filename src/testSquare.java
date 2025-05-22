import java.util.Scanner;

public class testSquare {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.println("Nhap kich thuoc canh hinh vuong:");
		float canh = sc.nextFloat();

		Square square = new Square(canh);
		square.hienThiCanh();
		square.tinhChuVi();
		square.tinhDienTich();
		System.out.println();
		square.hienThiTatCa();
	}
}
