import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Purchase {
	public void goPurchase() {
		Scanner s = new Scanner(System.in);
		System.out.println("받을 배송지를 입력하세요");
		String adress = s.nextLine();		
	}
	
	public static void printMap(Map<String, Integer> map) {
	    for (Map.Entry<String, Integer> entry : map.entrySet()) {
	        System.out.println("키: " + entry.getKey() + ", 값: " + entry.getValue());
	    }
	}
}
