package B4;

import java.util.ArrayList;
import java.util.Scanner;

public class News implements INews {
	private int id;
	private String tilte;
	private String publishDate;
	private String author;
	private String content;
	private float averageRate;
	private int[] rateList = new int[3];

	public News() {

	}

	public News(String tilte, String publishDate, String author, String content) {
		this.tilte = tilte;
		this.publishDate = publishDate;
		this.author = author;
		this.content = content;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getTilte() {
		return tilte;
	}

	public void setTilte(String tilte) {
		this.tilte = tilte;
	}

	public String getPublishDate() {
		return publishDate;
	}

	public void setPublishDate(String publishDate) {
		this.publishDate = publishDate;
	}

	public String getAuthor() {
		return author;
	}

	public void setAuthor(String author) {
		this.author = author;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

	public float getAverageRate() {
		return averageRate;
	}
	
	

	public int[] getRateList() {
		return rateList;
	}

	public void setRateList(int[] rateList) {
		this.rateList = rateList;
	}

	@Override
	public void display() {
		System.out.println("Tieu de: " + tilte);
		System.out.println("Ngay xuat ban: " + publishDate);
		System.out.println("Tac gia: " + author);
		System.out.println("Noi dung: " + content);
		System.out.println("Danh gia trung binh: " + averageRate);
	}

	public void calculate() {
		int tmp = 0;
		for (int i : rateList) {
			tmp += i;
		}
		averageRate = tmp / 3;
	}

	public static void main(String[] args) {
		int nhap;
		ArrayList<News> newArray = new ArrayList<News>();
		do {
			System.out.println();
			System.out.println(
					"1 – Insert news \r\n" + "2 – View list news \r\n" + "3 – Average rate \r\n" + "4 – Exit  ");
			Scanner sc = new Scanner(System.in);
			System.out.println("Nhap lua chon:");
			nhap = sc.nextInt();
			sc.nextLine();
			switch (nhap) {
			case 1:
				News news = new News();
				int[] rateList = new int[3];
				String tilte, publishDate, author, content;
				System.out.println("Nhap tieu de:");
				tilte = sc.nextLine();
				System.out.println("Nhap ngay phat hanh:");
				publishDate = sc.nextLine();
				System.out.println("Nhap tac gia:");
				author = sc.nextLine();
				System.out.println("Nhap noi dung:");
				content = sc.nextLine();
				System.out.println("Nhap 3 danh gia:");
				for(int i = 0;i<3;i++) {
					rateList[i] = sc.nextInt();
				}
				news.setTilte(tilte);
				news.setAuthor(author);
				news.setPublishDate(publishDate);
				news.setContent(content);
				news.setRateList(rateList);
				
				newArray.add(news);
				break;
			case 2:
				for (News i : newArray) {
					i.display();
				}
				break;
			case 3:
				for (News i : newArray) {
					i.calculate();
					i.display();
				}
				break;	
			default:
				break;
			}
		} while (nhap != 4);

		System.out.println("Da thoat chuong trinh");
	}

}
