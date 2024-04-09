import java.util.Scanner;

public class RunClass {
	public static void main(String[] args) {
		BuyList[] buyList = new BuyList[1000];
		int buyCount = 0;
		Scanner s = new Scanner(System.in);
		
		for(int i = 0; i< 9999; i++) {
			System.out.println("원하는 메뉴 선택");
			System.out.println("1. 구매");
			System.out.println("2. 구매내역 출력");
			System.out.println("q. 종료");
			
			String selectMenu = s.nextLine();
			if(selectMenu.equals("1")) {
				buyList[buyCount] = new BuyList();
				buyList[buyCount].order();
				buyCount++;
			}else if(selectMenu.equals("2")) {
				for(int j = 0; j < buyCount; j++) {
					System.out.println("no " + (j+1));
					System.out.println("상품명: " + buyList[j].goodsName);
					System.out.println("상품가격: " + buyList[j].price);
					System.out.println("배송지 " + buyList[j].address);
				}
			}else if(selectMenu.equals("q")) {
				break;
			}
		}
	}
}
