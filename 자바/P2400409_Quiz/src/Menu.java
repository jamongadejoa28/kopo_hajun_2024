import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Menu {
Map<String, Integer> menu = new HashMap<>();
	
	public void setMenu() {
		
		int price1 = 3000;
		int price2 = 1500;
		int price3 = 1000;
		String item1 = "양말";
		String item2 = "모자";
		String item3 = "가방";
		String item="";
		int price=0;
		int cnt1 = 0;
		int cnt2 = 0;
		int cnt3 = 0;
		Scanner s = new Scanner(System.in);
		while(true) {
			System.out.println("메뉴를 선택하세요");
			System.out.println("1: 양말, 2: 모자, 3: 가방");
			int input = s.nextInt();
			if(input==1)
			{
				item = item1;
				price = price1;
				cnt1++;
			}
			else if(input==2) {
				item = item2;
				price = price2;
				cnt2++;
			}
			else if(input==3) {
				item = item3;
				price = price3;
				cnt3++;
			}
			else if(input==0) {
				break;
			}
			menu.put(item, price);
		}
	}
	
	
}
