import java.util.Scanner;

public class B1 {
	public static void main(String[] args) {
		double a, b, c, delta;
		Scanner sc = new Scanner(System.in);
		do {
			System.out.println("Nhap he so a (a khac 0):");
			a = sc.nextDouble();
		} while (a == 0);
		System.out.println("Nhap he so b;");
		b = sc.nextDouble();
		System.out.println("Nhap he so c;");
		c = sc.nextDouble();

		delta = b * b - 4 * a * c;

		if (delta > 0)
			System.out.println("Can delta la:" + Math.sqrt(delta));
		else if (delta < 0)
			System.out.println("Phuong trinh vo nghiem");
		else
			System.out.println(0);
		;
	}
}
