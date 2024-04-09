import java.util.Scanner;

//구매내역
public class BuyList {
	String goodsName;
	int price;
	String address;

	// 구매한 상품 표시

	public void order() {
		Scanner s = new Scanner(System.in);
		System.out.println("구매할 상품을 선택해 주세요");
		System.out.println("1.양말");
		System.out.println("2.티셔츠");
		System.out.println("3.넥타이");
		System.out.println("4.자켓");
		String inputText = s.nextLine();
		
		if(inputText.equals("1")) {
			this.goodsName = "양말";
			this.price = 1000;
		}else if(inputText.equals("2")) {
			this.goodsName = "티셔츠";
			this.price = 2000;
		}else if(inputText.equals("3")){
			this.goodsName = "넥타이";
			this.price = 3000;
		}else if(inputText.equals("4")) {
			this.goodsName = "자켓";
			this.price = 4000;
		}else {
			System.out.println("입력이 잘못 되었습니다");
			return;
		}
		System.out.println("배송할 주소를 입력해주세요");
		this.address = s.nextLine();
	}
}
