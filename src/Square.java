
public class Square {

	private float canh;

	public Square(){
	}
	
	public Square(float canh) {
		this.canh = canh;
	}

	public float getCanh() {
		return canh;
	}

	public void setCanh(float canh) {
		this.canh = canh;
	}

	public void hienThiCanh() {
		System.out.println("Kich thuoc canh hinh vuong la:" + canh);
	}

	public void tinhDienTich() {
		System.out.println("Dien tich hinh vuong la:" + canh * canh);
	}

	public void tinhChuVi() {
		System.out.println("Chu vi hinh vuong la:" + canh * 4);
	}

	public void hienThiTatCa() {
		hienThiCanh();
		tinhChuVi();
		tinhDienTich();
	}

}
